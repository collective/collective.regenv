# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 2.0.0a1 (2026-02-23)


### Breaking changes:

- Drop support for Python 2.7. @ericof 
- Drop support for Python 3.8. @ericof 
- Drop support for Python 3.9. @ericof 
- Drop support to Plone 5.2. @ericof 


### New features:

- Add support for Python 3.12. @ericof 
- Add support for Python 3.13. @ericof 
- Add support to Plone 6.1 @ericof 
- Add support to Plone 6.2 @ericof 
- Drop support for Python 3.10. @ericof 


### Internal:

- Update package structure to match the latest template adopted by the Plone community. @ericof [#8](https://github.com/collective/collective.regenv/issues/8)


### Tests

- Use pytest instead of unittest. @ericof 

## 1.0.1 (unreleased)

- Added a viewlet that warns the admins that the site is using collective.regenv. @ale-rt


## 1.0.0 (2023-11-15)

- Add another environment variable to get the YAML file content from. @erral

## 1.0.0rc1 (2023-03-21)

- Get overridden keys more efficiently. @maurits

- Fix ``python_requires`` metadata. @maurits


## 1.0.0a2 (2022-12-27)

- Fix monkeys init. @mamico


## 1.0.0a1 (2022-12-27)

- Initial release. @mamico
