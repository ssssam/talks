title: Setting up OpenQA testing for GNOME
class: animation-fade
layout: true

<!--
OpenQA testing for GNOME
FOSDEM 2023 - Testing and Automation Devroom - Sunday 5/Feb 11:00
https://fosdem.org/2023/schedule/event/openqa_for_gnome/
25 minutes inc. questions and changeover.
-->

.bottom-bar[
{{title}}
]

---

# {{title}}

## Sam Thursfield <br /><tt>&lt;sam@afuera.me.uk&gt;</tt>

---

<!-- 1. About me / about GNOME -->

# About me

  * ~20 years involved in GNOME
  * ~10 years involved in Codethink

---

# About GNOME

GNOME is a graphical desktop environment with an open development model.

GNOME is older than:

  * FOSDEM (2000)
  * Wikipedia (2001)
  * Billie Eilish (2001)
  * Greta Thunberg (2003)
  * Facebook, Ubuntu (2004)
  * Git (2005)
  * Codethink (2008)
  * some of its contributors

---

<!-- 2. Why is GNOME hard to test? -->

# Why is GNOME hard to test?

 * Designed as a whole
 * Released as a kit of parts (200+ modules)

<!-- Photo of some Ikea furniture stress -->

---

# Why is GNOME hard to test?

No "BDFL".

https://wiki.gnome.org/Governance

"Each GNOME component (or "module") has one or more maintainers, and they generally have the final say over which changes are included in their components."

 * Unit tests are easy
 * Integration testing is harder - who is responsible when the tests fail?

???

Ref: conway's law

Open (public) development: various corps. and volunteers collaborate in the open

---

# Why is GNOME hard to test?

Who is responsible for integration testing?

[![](https://mermaid.ink/img/pako:eNqtlF1vmzAUhv-K5d4CSmyTApMmbcp2tWpT290s5OIEDgGVr9lGaxblv88G2gwl7VqtRqDD4Xlfm8PBe5o0KdKIbiW0OflyHdfEjCWqYlvfIlSrISQ2XhPXHW6V674nV03alXgFRa3NiXK-GjLkmFr_hx17Wzv-tnZi5XmeMbCHNTkphpHfgtxAWVr5NZYICvtJxniY5byaPak-z_NX8uIZflD8lTqyfSWWhdKyYasPMsnJN0juYItSrV8mm5sSbwqoXy3kj_XuP9lgZsivN5b5rmz72ev6aYCdAmwC8H8B4hTgE8CfrLL3JK73sdsSiW0jteud-2-OtG_ozwi6k2gUPztUg-TYokPHWUVSglJLzEiKGXSlJllRltFF1g_Hru0OowvO-Ri7v4pU5xFr799N5K1sElTq5fKHRAoqBylhFxFB-NQU2nY0TAVmweb59ZBxUIdWKCsoUrMj7a1hTHWOFcY0MuH4ojGN64NBuzYFjZ_SQjeSRhmUCh0KnW5udnVCIy07fICWBZgNrnqkWqhptKf3NJpz3wuChc9mPPAvBWMO3dls6C38meALMZvzxSU7OPR30xiDmaF9Fgoe-qFgQRj6vduP_qGd8vAHlyjAVw?type=png)](https://mermaid.live/edit#pako:eNqtlF1vmzAUhv-K5d4CSmyTApMmbcp2tWpT290s5OIEDgGVr9lGaxblv88G2gwl7VqtRqDD4Xlfm8PBe5o0KdKIbiW0OflyHdfEjCWqYlvfIlSrISQ2XhPXHW6V674nV03alXgFRa3NiXK-GjLkmFr_hx17Wzv-tnZi5XmeMbCHNTkphpHfgtxAWVr5NZYICvtJxniY5byaPak-z_NX8uIZflD8lTqyfSWWhdKyYasPMsnJN0juYItSrV8mm5sSbwqoXy3kj_XuP9lgZsivN5b5rmz72ev6aYCdAmwC8H8B4hTgE8CfrLL3JK73sdsSiW0jteud-2-OtG_ozwi6k2gUPztUg-TYokPHWUVSglJLzEiKGXSlJllRltFF1g_Hru0OowvO-Ri7v4pU5xFr799N5K1sElTq5fKHRAoqBylhFxFB-NQU2nY0TAVmweb59ZBxUIdWKCsoUrMj7a1hTHWOFcY0MuH4ojGN64NBuzYFjZ_SQjeSRhmUCh0KnW5udnVCIy07fICWBZgNrnqkWqhptKf3NJpz3wuChc9mPPAvBWMO3dls6C38meALMZvzxSU7OPR30xiDmaF9Fgoe-qFgQRj6vduP_qGd8vAHlyjAVw)

(Note! Many important teams aren't listed)

???

e.g. a change in gnome-control-centre, which depends on a change in systemd... which is not even in gnome, nor on all target OSes

---

<!-- 3. Integration testing 1999 -->

# Testing GNOME releases - 1999 style

Maintainer:

```bash
make test

sudo make install

make dist
```

Release team: "It builds... ship it!"

Distros: "It's released - ship it!"

Users: ...

---

# Issues with the 1999 model

Minimal integration testing.

Bugs introduced at integration time, reported upstream

  * "This only works if you pass `--enable-libfoo` at configure time..."

<!-- 4. 23 years of improvements -->

---
# Time passes

jhbuild
Meson
BuildStream

# Time passes

Git!
Gitlab!

CI is easy to setup for the first time.

---
# Time passes

"Testable" initiative.

  * OSTree
  * GNOME Continuous
  * gnome-build-meta
  * GNOME OS

---
# GNOME OS

Idea is [10 years old](https://blogs.gnome.org/aday/2012/08/07/gnome-os/)

Aims:

  * Provide a "known good" system
  * Allow automated regression testing
  * Allow designers and developers to test in-progress changes in a real system

???

"Known good" is very useful when debugging to see if the issue is in GNOME itself, or downstream.

---

<!-- 5. Integration testing 2022 -->

# Testing GNOME releases - 2022 style

Module contributors:

  * Send MR's, run automated tests, merge to 'master'
  * Update gnome-build-meta integration repo (usually)
  * Release tarballs

Release team:

  * Check full builds in gnome-build-meta CI
  * Build GNOME OS images
  * Publish tarballs

Distros:

  * Downstream regression testing (unit + integration tests)
  * Beta releases

Users:

  * Bug reports
  * Friendly messages thanking volunteers for their hard work

---

<!-- 6. Issues with this model -->

# Remaining issues

Only a few people test GNOME OS today

  * Building GNOME OS images takes hours
  * Easier to test "in-place" on development machine

"Unstable" releases happen, but nobody tests those either.

User bug reports are nice, but:

  * if you're not a domain expert, it's hard to produce an actionable bug report
  * distro packages can be very old, few folk enjoy maintaining old versions of their module
  * some distros add downstream patches with additional bugs

---

<!-- 7. Meanwhile downstream... -->

# OpenSuSE Tumbleweed

The first "rolling release" distro ?

Born [in 2010](http://www.h-online.com/open/news/item/openSUSE-Rolling-release-project-Tumbleweed-proposed-1146308.html), reworked heavily [in 2014](https://www.linux-magazine.com/Issues/2016/183/OpenSUSE-Tumbleweed).

Incoming packages from "Factory" put through regression testing using [OpenQA](https://open.qa/), then promoted.

???

Rolling release distro was a new idea in 2010, nobody did that.

# OpenQA

Initial commit in 2010.

Components:

  * Web interface (OpenQA)
  * Test driver (os-autoinst)
  * Test library (os-autoinst-distri-opensuse)

---

# OpenQA is used by...

 * OpenSUSE (?? tests)
 * SUSE
 * Fedora (?? tests)
 * EuroLinux (CentOS derivative)
 * Codethink (testing Linux)
 * Automotive industry (look out for QED)
 * ...

???

Who is familiar with OpenQA in the audience?



---

# Scale of GNOME

Design team: 16 people (Gitlab) - https://gitlab.gnome.org/groups/Teams/Design/-/group_members

Release team: 10 people (Gitlab) - https://gitlab.gnome.org/groups/Teams/Releng/-/group_members

"Official" modules: https://gitlab.gnome.org/GNOME : 20\*18 = 360 (core modules are less)

Gitlab - GNOME group = 290 developers who can commit.

https://hpjansson.org/blag/2022/07/23/gnome-at-25-a-health-checkup/

 * <1,400 contributors in 2021

Comparisons:
  
  * MS Windows: 227K MS employees (LinkedIn) - 1% on Windows = 2.7K contributors
  * Apple: 174K (Wikipedia) - 1% on OSX = 1.74K contributors

---

# GNOME development model

Design team:

  * new designs

Users:

  * issue reports
  * wish requests
  * ranting, etc.

Module maintainers: 

  * 6 months of work to implement those changes

Release team:

  * spin tarballs and upload to ftp.gnome.org

Distributions:

  * build tarballs and produce OS images

Users:

  * use the distro and find a bug

---

# Testing in 1999

If it builds, ship it!

* Works on my machine

`make test`

`./configure --prefix=/usr; make; make install`

Was f'in hard to do anything in that time... machines 100% slower, autotools, C'99 wasn't even invented

---

# Testing in 2023

https://about.gitlab.com/blog/2020/09/08/gnome-follow-up/

"Another noticeable difference in the community is that, since moving to GitLab, there is more awareness around what CI/CD is and how important it is to the development process. CI/CD is being used extensively throughout the project."

 * Gitlab CI is great

GNOME is designed as a whole, but built and shipped as a kit of parts.

???

Typical bug report: https://discourse.gnome.org/t/gnome-global-search-doesnt-find-any-files-in-my-native-language/13061/9

Result: fix compile flags for gnome-shell in Arch Linux


---

# Testing in 2023

Still:

  * Module CI
  * Release tarballs
  * ship to distros
  * Users test it and report bugs

???

    

---

# GNOME OS

What is GNOME OS?

  * The product of a 10-year initiative to make GNOME "Testable"
  * A bootable OS image built from "bleeding edge" GNOME components
  * Insecure and full of bugs - that's the point!
  * Defined in a single Git repository (gnome-build-meta)
  * Image-based deployment with read-only /usr and rollback

Nobody is volunteering to handle security issues, hardware enablement, user support.

---

# GNOME OS

Goals:

  * Allow designers and developers to test changes in real context
  * Control the whole stack - bootloader, kernel, userspace, toolchain - to provide "known good" reference system
  * ...

???

I'll go into the history of GNOME OS later

---

# GNOME OS Build process

Diagram here.

---

# Adding OpenQA testing

OpenQA workers are often bare metal

We want low maintenance overhead - use a Gitlab runner.

# 


# How did we get here? (Credits)

2012 - Colin Walters introduces OSTree, and GNOME Continuous


https://blogs.gnome.org/aday/2012/08/07/gnome-os/



class: impact

# Any questions?
