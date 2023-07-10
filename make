#!/usr/bin/env python3

"""Sam's reveal.js wrapper tool, version 99."""

from argparse import ArgumentParser, FileType
from dataclasses import dataclass, field
from io import BytesIO
from markdown import Markdown
from pathlib import Path
from typing import *
from zipfile import ZipFile
import logging
import os
import re
import sys
import time

from requests.exceptions import ConnectionError
import requests


log = logging.getLogger()


REVEAL_JS_VERSION = '4.4.0'
REVEAL_JS_URL = f"https://github.com/hakimel/reveal.js/archive/refs/tags/{REVEAL_JS_VERSION}.zip"


SEPARATOR_SLIDE = "---"
SEPARATOR_NESTED_SLIDE = "----"
SEPARATOR_NOTES = "???"


SECTION_TEMPLATE = """
<section>
  {content}
  {nested_slides}
</section>
"""


def argument_parser():
    parser = ArgumentParser(description="reveal.js wrapper tool")
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help="Enable detailed logging to stderr")
    parser.add_argument('--template', type=Path, default="template.html")
    parser.add_argument(
        '--watch', action='store_true', dest='watch',
        help="Run continuously and rebuild when inputs change."
    )
    parser.add_argument(
        '--no-watch', action='store_false', dest='watch',
        help="Run continuously and rebuild when inputs change."
    )
    parser.add_argument('infile', type=Path, nargs="?", default="presentation.md")
    parser.add_argument('outdir', type=Path, nargs="?", default="./output")
    return parser


def ensure_outdir(outdir):
    outdir.mkdir(exist_ok=True, parents=True)
    return outdir


def unzip(stream: BytesIO, outdir: Path, strip_components: int=0):
    """Extract a zipfile, allowing you to strip components from the path."""
    with ZipFile(stream) as zipfile:
        for zip_info in zipfile.infolist():
            path_in_zip = Path(zip_info.filename)
            if len(path_in_zip.parts) <= strip_components:
                log.debug(f"Ignore {path_in_zip}")
            else:
                extracted_path = Path('')
                extracted_path = extracted_path.joinpath(*path_in_zip.parts[strip_components:])
                log.debug(f"Made {extracted_path} from {path_in_zip.parts[strip_components:]}")

                # FIXME check its safe, the path might be malicious...
                log.debug(f"Extract {path_in_zip} as {extracted_path}")
                if zip_info.is_dir():
                    outdir.joinpath(extracted_path).mkdir()
                else:
                    zip_info.filename = str(extracted_path)
                    zipfile.extract(zip_info, outdir)


def download_and_unpack_reveal_js(outdir: Path):
    log.info(f"Fetch and extract {REVEAL_JS_URL}")
    try:
        response = requests.get(REVEAL_JS_URL);
        stream = BytesIO(response.content)
        unzip(stream, outdir, strip_components=1)
    except ConnectionError as e:
        raise RuntimeError(
            f"Unable to fetch reveal.js.\n"
            f"URL: {REVEAL_JS_URL}\n"
            f"Error: {e}")


@dataclass
class Slide:
    index: str
    markdown: str = field(default_factory=list)
    notes: Optional[str] = field(default_factory=list)
    nested_slides: List[object] = field(default_factory=list)


class SlideshowParser:
    def __init__(self):
        self._slides = []

        # Markdown extensions:
        #
        #   * attr_list: https://python-markdown.github.io/extensions/attr_list/
        #   * fenced_code: https://python-markdown.github.io/extensions/fenced_code_blocks/
        #   * md_in_html: https://python-markdown.github.io/extensions/md_in_html/
        #
        self._markdown_parser = Markdown(
            extensions=['attr_list', 'fenced_code', 'md_in_html'],
            output_format='html5'
        )

    def load_document(self, document: str):
        """Parse input document into the individual slides."""
        current_parent_slide = None
        notes = False

        log.debug(f"New slide {1}")
        current_slide = Slide(index="1")
        for line in document.splitlines():
            if line == SEPARATOR_SLIDE:
                if current_parent_slide:
                    current_parent_slide.nested_slides.append(current_slide)
                    log.debug(f"Slide {current_parent_slide.index} now has {len(current_parent_slide.nested_slides)} children")
                    self._slides.append(current_parent_slide)
                    current_parent_slide = None
                else:
                    self._slides.append(current_slide)
                current_slide = Slide(index=f"{len(self._slides)+1}")
                notes = False
                log.debug(f"New slide {current_slide.index}")
            elif line == SEPARATOR_NESTED_SLIDE:
                if current_parent_slide is None:
                    current_parent_slide = current_slide
                else:
                    current_parent_slide.nested_slides.append(current_slide)
                index = f"{current_parent_slide.index}.{len(current_parent_slide.nested_slides)+1}"
                current_slide = Slide(index=index)
                notes = False
                log.debug(f"New nested slide {index}")
            elif line == SEPARATOR_NOTES:
                log.debug(f"Notes for slide {current_slide.index}")
                notes = True
            else:
                if notes:
                    current_slide.notes.append(line)
                else:
                    current_slide.markdown.append(line)
        self._slides.append(current_slide)

    def _remove_paragraph_around_images(self, html) -> str:
        # See
        # https://stackoverflow.com/questions/24456010/in-markdown-is-there-a-way-to-stop-images-from-being-wrapped-with-p-tags
        # etc.
        #
        # Whatever is "correct" i don't care, this shit breaks `r-stretch` attr.
        html, _count = re.subn(r'<p>(<img[^>]*>)</p>', r'\1', html)
        return html

    def _convert_slides_to_html(self, slides: List[Slide]) -> str:
        # Convert a set of slides to HTML.
        result = []
        for slide in slides:
            log.debug(f"Convert slide {slide.index} to HTML")
            self._markdown_parser.reset()

            slide_markdown = '\n'.join(slide.markdown)
            slide_html = self._markdown_parser.convert(slide_markdown)

            nested_slides_html = ""
            if slide.nested_slides:
                nested_slides_html = self._convert_slides_to_html(slide.nested_slides)

            section_html = SECTION_TEMPLATE.format(
                content=slide_html,
                nested_slides=nested_slides_html,
            )

            section_html = self._remove_paragraph_around_images(section_html)

            result.append(section_html)
        return '\n'.join(result)

    def to_html(self) -> str:
        return self._convert_slides_to_html(self._slides)


def build(infile, template, outdir):
    document = infile.read_text()

    slideshow_parser = SlideshowParser()
    slideshow_parser.load_document(document)

    sections_text = slideshow_parser.to_html()

    template_text = template.read_text()
    output = template_text.replace('{{sections}}', sections_text)

    index = outdir.joinpath('index.html')
    index.write_text(output)
    log.info(f"Wrote {index}")


def watch(infile, template, outdir):
    infile = Path(infile)
    template = Path(template)

    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        raise RuntimeError("The 'watchdog' PyPI package is needed for `--watch` mode")

    class EventHandler(FileSystemEventHandler):
        def on_modified(self, event):
            log.debug(f"Event: {event}")
            event_path = Path(event.src_path)
            if event_path.samefile(infile) or event_path.samefile(template):
                log.info(f"Change to {event_path}, rebuilding")
                # FIXME: we get multiple events quickly and we should debounce
                # these, but that requires an event loop or background thread.
                build(infile, template, outdir)

    observer = Observer()
    paths = set([infile.parent, template.parent])
    for path in paths:
        observer.schedule(EventHandler(), path)

    log.info(f"Watching locations for changes: {[str(p) for p in paths]}. Press CTRL+C to exit.")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    args = argument_parser().parse_args()

    if args.debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)


    outdir = ensure_outdir(args.outdir)
    if not outdir.joinpath('js/reveal.js').exists():
        download_and_unpack_reveal_js(outdir)

    build(args.infile, args.template, outdir)
    if args.watch:
        watch(args.infile, args.template, outdir)

#try:
main()
#except RuntimeError as e:
#    sys.stderr.write("ERROR: {}\n".format(e))
#    sys.exit(1)
