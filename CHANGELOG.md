# Change Log

## 0.6 (unreleased)

### Summary

- [#173](https://github.com/awslabs/amazon-s3-find-and-forget/pull/173): Show
  column types and hierarchy in the front-end during Data Mapper creation
- [#173](https://github.com/awslabs/amazon-s3-find-and-forget/pull/173): Add
  support for char, smallint, tinyint, double, float

## v0.5

### Summary

- [#172](https://github.com/awslabs/amazon-s3-find-and-forget/pull/172): Fix for
  an issue where Make may not install the required Lambda layer dependencies,
  resulting in unusable builds.

## v0.4

### Summary

- [#171](https://github.com/awslabs/amazon-s3-find-and-forget/pull/171): Fix for
  a bug affecting the API for 5xx responses not returning the appropriate CORS
  headers

## v0.3

### Summary

- [#164](https://github.com/awslabs/amazon-s3-find-and-forget/pull/164): Fix for
  a bug affecting v0.2 deployment via CloudFormation

## v0.2

### Summary

- [#161](https://github.com/awslabs/amazon-s3-find-and-forget/pull/161): Fix for
  a bug affecting Parquet files with nullable values generating a
  `Table schema does not match schema used to create file` exception during the
  Forget phase

## v0.1

### Summary

Initial Release
