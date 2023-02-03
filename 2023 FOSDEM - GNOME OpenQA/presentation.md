<!--
OpenQA testing for GNOME
FOSDEM 2023 - Testing and Automation Devroom - Sunday 5/Feb 11:00
https://fosdem.org/2023/schedule/event/openqa_for_gnome/
25 minutes inc. questions and changeover.
-->

# Setting up OpenQA testing for GNOME

<div class="r-stretch"></div>

<div class="flex-row-stretch" markdown="1">
  <p class="left" style="flex: 1;" markdown="1">
  **Sam Thursfield**<br>
  **FOSDEM 2023**
  </p>

  ![Codethink logo](./images/codethink-logo.svg){:.right style="flex: 1;"}
</div>

---

<!-- 1. About me / about GNOME -->

## About me

  * ~20 years involved in GNOME
  * ~10 years involved in Codethink

![Me playing trombone on a tram](./images/photo-2014.jpg){:height="500px"}

???

Codethink are a consultancy, work in automotive helping to improve automotive testing pipelines - hence OpenQA interest.

---

## About GNOME

GNOME is a graphical desktop environment with an open development model.

<img alt="GNOME overview" src="images/gnome.png" class="r-stretch">

---

## GNOME is older than ...

<div class="flex-row-stretch">
<div>
<img alt="FOSDEM logo" src="images/fosdem-logo.png" style="height: 1em;"> (2000)<br>
</div>
<div>
<img alt="Ubuntu logo" src="images/ubuntu-logo.png" style="height: 1em;"> (2004)<br>
</div>
<div>
<img alt="Git logo" src="images/git-logo.svg" style="height: 1em;"> (2005)<br>
</div>
<div>
<img alt="Android logo" src="images/android-logo.svg" style="height: 1em;"> (2005)<br>
</div>
</div>

<!--  * Billie Eilish (2001)
  * Myspace (2003)
  * Greta Thunberg (2003)
  * Codethink (2008)
  * Golang, Rust
  * some of its contributors
-->

---

<!-- 2. Why is GNOME hard to test? -->

<h2 class="r-fit-text">GNOME is hard to test</h2>

 * Designed as a whole
 * Released as a kit of parts (200+ modules)

<img src="images/jigsaw.jpg">

???

Also - cruft
Also - inconsistent investment around upstream testing, volunteers not super interested in testing

---

**Who is responsible for integration testing?**
{:.fs-3}

<!--
[![](https://mermaid.ink/img/pako:eNqtlF1vmzAUhv-K5d4CSmyTApMmbcp2tWpT290s5OIEDgGVr9lGaxblv88G2gwl7VqtRqDD4Xlfm8PBe5o0KdKIbiW0OflyHdfEjCWqYlvfIlSrISQ2XhPXHW6V674nV03alXgFRa3NiXK-GjLkmFr_hx17Wzv-tnZi5XmeMbCHNTkphpHfgtxAWVr5NZYICvtJxniY5byaPak-z_NX8uIZflD8lTqyfSWWhdKyYasPMsnJN0juYItSrV8mm5sSbwqoXy3kj_XuP9lgZsivN5b5rmz72ev6aYCdAmwC8H8B4hTgE8CfrLL3JK73sdsSiW0jteud-2-OtG_ozwi6k2gUPztUg-TYokPHWUVSglJLzEiKGXSlJllRltFF1g_Hru0OowvO-Ri7v4pU5xFr799N5K1sElTq5fKHRAoqBylhFxFB-NQU2nY0TAVmweb59ZBxUIdWKCsoUrMj7a1hTHWOFcY0MuH4ojGN64NBuzYFjZ_SQjeSRhmUCh0KnW5udnVCIy07fICWBZgNrnqkWqhptKf3NJpz3wuChc9mPPAvBWMO3dls6C38meALMZvzxSU7OPR30xiDmaF9Fgoe-qFgQRj6vduP_qGd8vAHlyjAVw?type=png)](https://mermaid.live/edit#pako:eNqtlF1vmzAUhv-K5d4CSmyTApMmbcp2tWpT290s5OIEDgGVr9lGaxblv88G2gwl7VqtRqDD4Xlfm8PBe5o0KdKIbiW0OflyHdfEjCWqYlvfIlSrISQ2XhPXHW6V674nV03alXgFRa3NiXK-GjLkmFr_hx17Wzv-tnZi5XmeMbCHNTkphpHfgtxAWVr5NZYICvtJxniY5byaPak-z_NX8uIZflD8lTqyfSWWhdKyYasPMsnJN0juYItSrV8mm5sSbwqoXy3kj_XuP9lgZsivN5b5rmz72ev6aYCdAmwC8H8B4hTgE8CfrLL3JK73sdsSiW0jteud-2-OtG_ozwi6k2gUPztUg-TYokPHWUVSglJLzEiKGXSlJllRltFF1g_Hru0OowvO-Ri7v4pU5xFr799N5K1sElTq5fKHRAoqBylhFxFB-NQU2nY0TAVmweb59ZBxUIdWKCsoUrMj7a1hTHWOFcY0MuH4ojGN64NBuzYFjZ_SQjeSRhmUCh0KnW5udnVCIy07fICWBZgNrnqkWqhptKf3NJpz3wuChc9mPPAvBWMO3dls6C38meALMZvzxSU7OPR30xiDmaF9Fgoe-qFgQRj6vduP_qGd8vAHlyjAVw)
-->
![Diagram of designer -> maintainer -> release team -> packager flow](./images/mermaid1.png)

???

(Note! Many important teams aren't listed)
No "BDFL".
Ref: conway's law
Unit tests are easy

Open (public) development: various corps. and volunteers collaborate in the open

e.g. a change in gnome-control-centre, which depends on a change in systemd... which is not even in gnome, nor on all target OSes

---

<!-- 3. Integration testing 1999 -->


**Release process, 1999**{:.r-fit-text}

<div class="left fs-3" markdown="1">
👷 <span class="highlight">**Maintainer**</span>: *"It works on my machine!"*

👩 <span class="highlight">**Release team**</span>: *"It builds... ship it!"*

🧔 <span class="highlight">**Distributions**</span>: *"A new upstream release - ship it!"*

👼<span class="highlight">**Users**</span>: Time to test if anything works...

[!["Works on my machine" certificate](images/works_on_my_machine.jpg){:width=150px height=150px}](https://blog.codinghorror.com/the-works-on-my-machine-certification-program/)
{:.center}

Many "bugs" appear at integration time.

???

Minimal integration testing, downstream integration is very hard to get right.

> "This feature only works if you pass `--enable-ibus` at configure time..."
{:.fs-5}

</div>

<!-- 4. 23 years of improvements -->

---
# Time passes

* New **build tools** (*jhbuild*, *Meson*, *BuildStream*, ...)
* New **collaboration tools** (*Git*, *Gitlab*, ...)
* **CI** becomes practical

🕘
{:style="font-size: 120px"}

???

24 years!

empires grow and crumble, everyone gets a smartphone, 5 versions of MS Windows, AI takes all our jobs and we no longer have to work...

https://about.gitlab.com/blog/2020/09/08/gnome-follow-up/

"Another noticeable difference in the community is that, since moving to GitLab, there is more awareness around what CI/CD is and how important it is to the development process. CI/CD is being used extensively throughout the project."

---
**Release process, 2023**{:.r-fit-text}

<div class="left fs-3" markdown="1">
👷 <span class="left highlight">**Maintainer**</span>: Review merge requests, check tests

👵 <span class="highlight">**Release team**</span>: Update and check integration repo ([gnome-build-meta](https://gitlab.gnome.org/gnome/gnome-build-meta))
{:.r-fit-text}

👴 <span class="highlight">**Distributions**</span>: Downstream regression testing

👩👱<span class="highlight">**Users**</span>: Friendly messages thanking volunteers for their hard work
{:.r-fit-text}
</div>

There's still a large gap between 'main' branch and distro releases.

???

Most components are unit-tested (not all.. volunteers don't work on getting 100% test coverage)
Some distros do whole-system testing (some still pass on regressions straight to users :-), OpenSUSE Tumbleweed a pioneer.

 * Distros test tarball releases, alpha tarball could have months of new development
 * Distro developers aren't domain experts, so they don't always provide the best bug reports.

OpenSuSE Tumbleweed: The first "rolling release" distro ?

Born [in 2010](http://www.h-online.com/open/news/item/openSUSE-Rolling-release-project-Tumbleweed-proposed-1146308.html), reworked heavily [in 2014](https://www.linux-magazine.com/Issues/2016/183/OpenSUSE-Tumbleweed).

Incoming packages from "Factory" put through regression testing using [OpenQA](https://open.qa/), then promoted.

Rolling release distro was a new idea in 2010, nobody did that.

---

What if GNOME had its own distro built from 'main' branches?


---
# GNOME OS

<div class="fs-3 left" markdown="1">
Part of the ["Testable" initiative](https://blogs.gnome.org/aday/2012/08/07/gnome-os/) (*OSTree*, *GNOME Continuous*, *gnome-build-meta*, ...)
{:.r-fit-text}

**Goals**:

  * Provide a "known good" full system integration
  * Allow designers and developers to test in-progress changes
  * Automated regression testing

**Non-goals**:

  * Reliability
  * Security updates, hardware enablement, user support
</div>


???

Idea is [10 years old](https://blogs.gnome.org/aday/2012/08/07/gnome-os/)

"Known good" is very useful when debugging to see if the issue is in GNOME itself, or downstream.

---

![Screenshot of os.gnome.org](images/gnome_os.png){:.r-stretch}

<https://os.gnome.org>

---

<!-- 6. Issues with this model -->

# GNOME OS

<div class="left fs-2" markdown="1">
Only a few people test GNOME OS today.

<div class="center" markdown="1">
🚲
{:style="font-size: 120px;"}
</div>

Building an OS image takes **several hours**.

How can we catching complex regressions *before* releasing tarballs?

</div>

???

Developers still test "in-place" on development machine as they need a faster cycle time.

<!-- 7. Meanwhile downstream... -->

---

**OpenQA**
{:.r-fit-text}

<div class="left" markdown="1">
Initial commit in 2010.

Components:

  * **Web interface** ([OpenQA](https://github.com/os-autoinst/openQA))
  * **Test driver** ([os-autoinst](https://github.com/os-autoinst/os-autoinst))
  * **Test library** ([os-autoinst-distri-opensuse](https://github.com/os-autoinst/os-autoinst-distri-opensuse))
</div>

???

Who is familiar with OpenQA in the audience?

---

# Who uses OpenQA?

 * OpenSUSE (<https://openqa.opensuse.org/>)
 * Fedora (<https://openqa.fedoraproject.org/>)
 * EuroLinux (CentOS derivative)
 * Codethink (<https://openqa.qa.codethink.co.uk/>)
 * Various Codethink clients in automotive industry
 * ...you?

???

OpenSUSE and SUSE Enterprise

---

----

**OpenQA: main page**

![openQA screenshot](./images/openqa-ui-main.png){:.r-stretch}

<https://openqa.gnome.org>

----

<!-- 8. Show and tell: viewing the tests -->

**Gitlab: gnome-build-meta repo**

![gnome-build-meta repo screenshot](images/gitlab-gbm.png){:.r-stretch}

<https://gitlab.gnome.org/gnome/gnome-build-meta>

???

GNOME release team's integration repo

"What repos and commits correspond to release X.Y of GNOME ?"

Lots of work done in CI pipelines. Two beefy donated servers (x86_64, ARM) run builds.

----

**Gitlab: gnome-build-meta wiki**

![gnome-build-meta wiki screenshot showing OpenQA docs](images/gitlab-gbm-wiki.png){:.r-stretch}

----

**Gitlab: CI pipelines**

![gnome-build-meta 'master' CI pipelines](images/gitlab-pipelines-master.png){:.r-stretch}

----

**Gitlab: s3-image**

![gnome-build-meta 's3-image' job](images/gitlab-pipeline-s3-image.png){:.r-stretch}

???

This job creates an installer ISO and uploads it to Amazon S3 file storage.

----

**Gitlab: test-s3-image**

![gnome-build-meta 'test-s3-image' job](images/gitlab-pipeline-test-s3-image.png){:.r-stretch}

???

This job runs the OpenQA tests

----

**Gitlab: test-s3-image**

<div class="r-stretch" markdown="1">
This job:

 * runs using the upstream 'openqa-worker' Docker image
 * downloads the ISO from S3
 * creates a temporary, unique 'machine' and connects it to OpenQA
 * submits a test job to OpenQA, tagging it with the unique machine ID
 * starts the 'run_worker' script in bg, and waits for the job
 * polls job status report until its passed/failed
 * job runs, against the locally downloaded ISO, and passes or fails
 * removes the machine again and pipeline exists
</div>

???

The runner *is* the worker - not a dedicated machine. (less infra to maintain- we already have this beefy server set up as a Gitlab runner, with sufficient privs to do KVM inside Docker).

<!-- 9. Show and tell: viewing the tests -->

---

----

**OpenQA: Test results**

![OpenQA test result - main](./images/openqa-ui-tests-top.png){:.r-stretch}

???

Each of these tests on the LHS corresponds to a Perl script in 'openqa_tests.git' repo.

----

**OpenQA: Test results**

![OpenQA test result - 2](./images/openqa-ui-tests-1.png){:.r-stretch}

----

**OpenQA**: `gnome_install` test

![OpenQA 'gnome\_install' test](./images/openqa-ui-needle-install.png){:.r-stretch}

???

What you see in the web UI are the screenshot comparisons ('needles')

Behind the scenes are test scripts written in Perl. We'll look at those later.

Helper functions provided by OpenQA to:

  * do screenshot ('needle') comparisons
  * send keypresses and mouse click events to QEMU display (over VNC)
  * needle can have 'click' areas to make this easier

----

**OpenQA**: `gnome_welcome` test

![OpenQA test creating 'testuser' account](./images/openqa-ui-needle-testuser.png){:.r-stretch}

???

First time we can log in (no root password)

----

**OpenQA**: `gnome_journal_capture_fix` test


![OpenQA running command over serial](./images/openqa-ui-serial.png){:.r-stretch}

???

Several ways to run commands - serial console is least extra work.

----

**OpenQA**: `gnome_desktop` test

![OpenQA needle matching GNOME Shell](./images/openqa-ui-needle-gnome-desktop.png){:.r-stretch}

???

Exclusion match: ignore version number.

Design changes: all needles with tag 'gnome_desktop_tour' are tried, and if any matches, test passes. So it tests against all old and new versions of the design. (You can remove old needles if you want).

----

**OpenQA**: `gnome_system_monitor` test

![OpenQA needle matching GNOME system monitor](./images/openqa-ui-needle-gnome-desktop.png){:.r-stretch}

???

Exclusion match: window body.

<!-- 10. Show and tell - needle editor -->

---
----

**OpenQA: needle editor**

![OpenQA needle editor](./images/openqa-ui-needle-editor-1.png){:.r-stretch}

----

**OpenQA: needle editor 2**

![OpenQA needle editor](./images/openqa-ui-needle-editor-2.png){:.r-stretch}

<!-- 11. Show and tell - openqa-needles and openqa-tests repos -->

----

**OpenQA: openqa-needles Git repo**

![openqa-needles.git repo](./images/openqa-needles.git.png){:.r-stretch}

???

All in one repo

Multiple versions of the product with design differences:

  * test everything against everything

Repo gets very big... no solution really.

----

**OpenQA: a needle**

<div class="flex-row-stretch" display="flex:1;" markdown="1">
<div markdown="1" style="width: 18em;">
```json
{
  "area": [
    {
      "xpos": 31,
      "ypos": 78,
      "width": 959,
      "height": 599,
      "type": "match"
    }
  ],
  "properties": [],
  "tags": [
    "app_baobab_home"
  ]
}
```
</div>
<div markdown="1">
![Baobab app screenshot](./images/app_baobab_home.png){:width=75%}
</div>
</div>

<!-- 11. Show and tell - openqa-tests and openqa-needles repos -->

----

**openqa-tests.git**

![openqa-tests.git repo](./images/openqa-tests.git.png){:.r-stretch}

???

Everything is Perl.

Python is supported in theory, i didn't get it to work, and it involves a Perl->Python bridge so additional complexity that might be unhelpful.

----

**openqa-tests/main.pm**

```
my $distri = testapi::get_required_var('CASEDIR') . '/lib/gnomeosdistribution.pm';
require $distri;
testapi::set_distribution(gnomeosdistribution->new);

$testapi::username = 'testuser';
$testapi::password = 'testingtesting123';

autotest::loadtest("tests/gnome_install.pm");
autotest::loadtest("tests/gnome_welcome.pm");
autotest::loadtest("tests/gnome_journal_capture_fix.pm");
autotest::loadtest("tests/gnome_disable_update_notification.pm");
...
```
<!-- ![main.pm](./images/tests-main.pm.png){:.r-stretch} -->

----

**openqa-tests/tests/gnome-install.pm**

```
use base 'basetest';
use strict;
use testapi;
use bootloader;

sub run {
    my $self = shift;

    bootloader_add_kernel_args(' console=ttyS0 systemd.journald.forward_to_console=1');

    assert_and_click('gnome_install_1', timeout => 120, button => 'left');
    assert_and_click('gnome_install_disk', timeout => 10, button => 'left');
    assert_and_click('gnome_install_disk2', timeout => 10, button => 'left');
    assert_screen('gnome_install_reformatting1', timeout => 120);
    assert_screen('gnome_install_complete', timeout => 180);
    eject_cd;
    power('reset');
}

sub test_flags {
    return { fatal => 1 };
}

1;
```
<!-- ![gnome-install.pm](./images/tests-gnome-install.pm.png){:.r-stretch} -->

----

**openqa-tests/tests/gnome-welcome.pm**

```
sub run {
    my $self = shift;

    assert_and_click('gnome_firstboot_welcome', timeout => 600, button => 'left');
    assert_and_click('gnome_firstboot_language', timeout => 10, button => 'left');
    assert_and_click('gnome_firstboot_privacy', timeout => 10, button => 'left');
    assert_screen('gnome_firstboot_timezone_1', 30);
    send_key('tab');
    type_string('London, East', wait_screen_change => 6, max_interval => SLOW_TYPING_SPEED);
    ...
```
<!-- ![gnome-welcome.pm](./images/tests-gnome-welcome.pm.png){:.r-stretch} -->

---

<!-- 12. OpenQA tips and tricks -->

## Tips and Tricks

<div markdown="1" class="fs-3">

1. OpenQA is great!  ❤️  Use it!

2. Explore the test library code:

    * [testapi docs](http://open.qa/api/testapi/)
    {: .fs-4 }
    * [os-autoinst-distri-opensuse](https://os-autoinst.github.io/os-autoinst-distri-opensuse/)
    {: .fs-4 }

3. Keep tests simple.

4. Always check the os-autoinst logs.

    * Example: If needle bounds are invalid, you get a log message and a "0% match" in web UI
    {: .fs-4 }

5. Learn how to run the testsuite locally.

6. Take care with upstream containers - pin versions using container hash.

</div>

<!-- 13. Next steps for GNOME -->

---

## Next steps for GNOME OpenQA

1. Build a small team to maintain tests and infra.

2. Reach "production ready" state.

3. GNOME module teams maintaining & extending their own tests.

4. Add example user content (text documents, multimedia, etc)

<!-- 14. Credits -->

---

## Credits

<div class="flex-row-stretch fs-6 left top" markdown="1">
<div markdown="1" style="margin-right: 2em">
Top names from gnome-continuous and gnome-build-meta repos:

 * Abderrahim Kitouni
 * Carlos Garcia Campos
 * Colin Walters
 * Debarshi Ray
 * Dor Askayo
 * Emmmanuele Bassi
 * Giovanni Campagna
 * Iñigo Martinez
 * Jasper St. Pierre
 * Javier Jardón
 * Jeremy Bicha
 * Jordan Petridis
 </div>
<div markdown="1" style="margin: 2em">
 * Michael Catanzaro
 * Owen Taylor
 * Philip Chimento
 * Tristan Van Berkom
 * Vadim Rutkovsky
 * Valentin David

Special mentions:

 * Allan Day (blogs, documentation)
 * Andrea Veri (OpenID help)
 * James Thomas (openQA tests & QEMU help)
 * Will Thompson (Endless installer, OpenQA advice, ...)
</div>
</div>
???

2012 - Colin Walters introduces OSTree, and GNOME Continuous

https://blogs.gnome.org/aday/2012/08/07/gnome-os/

<!-- 15. How to get involved / Q & A-->

---

## Codethink plans for 2023 {:.r-fit-text}

<div class="left" markdown="1">
  * Continue Linux mainline testing (OpenQA + LAVA)
  * **QAD**: open source tool to control hardware from OpenQA tests
  * Hardware **USB switcher** device

Follow us for details:

  * [@codethink@social.codethink.co.uk](https://social.codethink.co.uk/codethink) (Fediverse)
  * [@codethink](https://www.twitter.com/codethink) (Twitter)
  * [https://www.codethink.co.uk/](https://www.codethink.co.uk)

---

## How to get involved {:.r-fit-text}

<div class="left" markdown="1">

I will provide training on infra maintenance and writing tests - just ask!

  * Chat: Matrix [#gnome-os:gnome.org](https://app.element.io/#/room/#gnome-os:gnome.org) (Libera.chat #gnome-os)
  {:.fs-3}
  * Email: *sam@afuera.me.uk*
  {:.fs-3}
  * Forum: [https://discourse.gnome.org/](https://discourse.gnome.org/)
  {:.fs-3}

Also: [documentation](https://gitlab.gnome.org/GNOME/gnome-build-meta/-/wikis/openqa/OpenQA-for-GNOME-developers), [issue tracker](https://gitlab.gnome.org/GNOME/gnome-build-meta/-/wikis/openqa/OpenQA-for-GNOME-developers)
{:.fs-3}

<div class="flex-row-stretch" markdown="1">
  <p class="left" style="flex: 1;" markdown="1">
  **Sam Thursfield**<br>
  **FOSDEM 2023**
  </p>

  ![Codethink logo](./images/codethink-logo.svg){:.right style="flex: 1;"}
</div>
