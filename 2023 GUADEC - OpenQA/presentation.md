<!--
The best testing tools we've ever had
GUADEC 2023 - ...
... minutes
-->

### The best testing tools we've ever had {:.r-fit-text}

An introduction to
## openQA for GNOME {:.r-fit-text}

<div class="r-stretch"></div>

<div class="flex-row-stretch" markdown="1">
  <p class="left" style="flex: 1;" markdown="1">
  **Sam Thursfield**<br>
  **GUADEC 2023**
  </p>

  ![Codethink logo](./images/codethink-logo.svg){:.right style="flex: 1;"}
</div>

---

# My story

 * GNOME (2003-)
 * Codethink (2011-)
 * Desktop search (Tracker) (2011-)

???

I don't always do "about me", but it is relevant here to see why I've been pushing this recently...

Using GNOME since 2003 ([2.8](https://help.gnome.org/misc/release-notes/2.8/))

Codethink - somehow still work here - consultancy, mostly financial & automotive work now

Early projects: MeeGo - Tracker - critical bugs e.g. 100% CPU when you connect a USB stick.

No paid work on Tracker since 2012, but remained as a volunteer maintainer. Ported to Meson, set up initial Gitlab CI, in-tree "functional tests" testsuite.

---

## Dreams of end to end testing

 * GUADEC 2012 in A Coruña:
     * GNOME Continuous; "Testable" iniative
 * GNOME OS:
     * BuildStream, Freedesktop SDK)
 * openQA at SUSE: 2009
     * Now used by Fedora, Debian, and more
 * Codethink: openQA testing in automotive

???

We've been working towards "integration testing of GNOME as it happens" for over a decade.

---

Open this URL in your laptop:

<https://openqa.gnome.org/>
{:.r-fit-text}

![QR code](./images/qr-code.png){:.r-stretch}

???

You can sign in with GNOME LDAP if you have it.

View "All tests" and select one test

Do this in browser ! Show:

  -- install: 
  --   it's creating an empty qemu VM
  --   installing GNOME OS with the latest ISO
  --   ...
  -- apps:
  --   it uses the preinstalled disk image
  -->

---

Look at:

  1. gnome_install test
  2. gnome_apps test

---
class: left

# End to end testing of GNOME {:.r-fit-text}

**openQA** runs a test script on a device and takes screenshots.
{.highlight}

<div class="gray-2 fs-2" markdown="1">
  * Each testsuite runs in a new virtual machine
  * Tests run against [GNOME OS](https://os.gnome.org/):
     * Latest commit of every GNOME module
     * [Freedesktop SDK](https://gitlab.com/freedesktop-sdk/freedesktop-sdk/-/tree/master/elements) base OS
  * Working since Sept. 2022, in "open beta" status
</div>

???

Notes:

  * openQA manages VM (using QEMU); hardware testing can come soon
  * distro independent - distros are doing their own integration testing (many also using openQA), but testing already-released versions of GNOME
  * using Freedesktop SDK beta OS (~modern base, & we can control version of every component)
  * max ~1hr a week to maintain, infra (only me), tests (me + Jordan)
    * you're invited to join in!

---

## Types of testing

![](images/test-pyramid.webp)

???

Mike Cohn's "test pyramid" ("Succeeding with Agile").

  * Unit tests - easy to write; hard to test real usecases (everything outside the unit is "mocked", e.g. connect a USB stick)
  * Integration tests: everything else goes here.
      * "Functional tests", "UI tests", "service tests",...
  * I prefer "end to end testing" over "OS testing"
     * You control every aspect! Via mouse, keyboard, connect a real USB stick...
     * Good coverage of stuff which is difficult with project-specific tests: hardware support, initial setup, session management, font rendering ...
  * Test itself is fast & cheap; but *cycle time* is slow with openQA tests

---

## Types of testing

*openQA goes here*

  ⇓

![](images/test-pyramid.webp) 

???

Are they any open source alternatives ?

---

## Components of GNOME openQA testing {:.r-fit-text}

1. openQA Web UI -- optional
2. Gitlab `gnome-build-meta` repo -- builds GNOME OS image, & runs openQA tests
2. isotovideo -- test runner (you can run this on your laptop)
3. Testsuites (Perl scripts which use [test API](http://open.qa/api/testapi/))
4. Needles (screenshots)

---
class: left

## How your test controls the VM {:.r-fit-text}

1) Trigger an action:

<div class="fs-3 gray-2" markdown="1">
  * Type on keyboard - [`send_key`](http://open.qa/api/testapi/#_send_key), [`type_string`](http://open.qa/api/testapi/#_type_string)
  * Click with mouse - [`mouse_set`](http://open.qa/api/testapi/#_mouse_click),[`assert_and_click`](http://open.qa/api/testapi/#_click_lastmatch)
  * Run command on serial console - [`assert_script_run`](http://open.qa/api/testapi/#_assert_script_run)
  * Other stuff: [`power`](http://open.qa/api/testapi/#_power), [`switch_network`](http://open.qa/api/testapi/#_switch_network), ...
</div>

2) Assert that the correct thing happened

<div class="fs-3 gray-2" markdown="1">
  * Await needle (screenshot) match - [`assert_screen`](http://open.qa/api/testapi/#_assert_screen)
  * Other stuff - [`upload_asset`](http://open.qa/api/testapi/#_upload_asset), [`assert_recorded_sound`](http://open.qa/api/testapi/#_assert_recorded_sound), ...
</div>

???

You can run the tests on your laptop

You are not limited to screenshot testing.

Tests are Perl programs & can run arbitrary code. openQA is not only for screenshot tests.

But it has special helpers for screenshot testing. We'll go more into how that works.

---

 * How to:

     * Look at screenshots and see "latest GNOME"
     * Diagnose & report regressions in a component
     * Fix a test failure
     * Develop new test cases

???

Show some screenshots, explain "Needles".

---


---

Check the "Logs & Assets" tab

???

If you're a developer you're thinking, what do I do if this fails?

Obvious option: run the same OS image in gnome-boxes and reproduce the issue there

Quickest option: Look at the journal.

Show the serial0.txt log

Show link to Gitlab

---

# How it works

  * Gitlab pipeline for gnome-build-meta.git has a "test-s3-image" job
  * The runner registers as a temporary openQA worker
  * The test job is submitted to the web UI

???

This is a "non-standard" approach, which saves us from maintaining a fleet of physical runners.

---

# Here's what we can do today

  * Curate and browse screenshots of the next GNOME release
  * Run ~nightly tests as we develop new features

???

More ?

We can do integration testing of your latest GNOME modules from Git.

Let's write some tests!

But first... some notes on how we got here.

---

---

# How do you write integration tests for a search engine?

Golden rule: if it's not tested, it doesn't work.

Actual bug reports:

  * Performance issues on corporate deployment with NFS home directory
  * GStreamer enters 100% CPU usage when typefinding files in a video game mod due to trying to decode them as MP3
  * ...

Input: an entire hard disk of random data.

Actual tests: https://gitlab.gnome.org/GNOME/tracker-miners/-/blob/master/tests/functional-tests/test_fts_basic.py

???

I'll leave you with this problem...

---

## Questions

"How much effort is it to maintain?"

"How expensive is it to run?"

"Can distros do this for us?"

"How many 'real' bugs has it caught so far?"

"What's next?"

---

## How much effort is it to maintain? {:.r-fit-text}

![Graph of hours spent against date](images/Hours spent on openQA maintenance.svg){:.r-stretch}

Source: <https://gitlab.gnome.org/GNOME/openqa-tests/-/issues/9>
{:.fs-4}

---

## What's next?

It's up to you!

  * Core app developers: extend tests for your app/component
     * Can we move tests into module repos?
  * Organisations that can host hardware: devices for hardware testing
  * Infra experts: help maintain web UI 
  * Everyone:
     * Subscribe to gnome-build-meta pipeline failures
     * Add tests for accessibility features
     * Add tests for other locales (e.g. Turkish)
     * Contribute to example-test-content

---


## How to get involved {:.r-fit-text}

<div class="left" markdown="1">

I will provide training on infra maintenance and writing tests - just ask!

  * Chat: Matrix [#gnome-os:gnome.org](https://app.element.io/#/room/#gnome-os:gnome.org)
  {:.fs-3}
  * Forum: [https://discourse.gnome.org/](https://discourse.gnome.org/)
  {:.fs-3}
  * Email: *sam@afuera.me.uk*
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
</div>
