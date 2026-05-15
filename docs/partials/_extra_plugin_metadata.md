<!-- markdownlint-disable MD041 -->
## Additional metadata

When packaging the plugin, some extra metadata information can be added if these keys are present in the `metadata.txt`:

* `commitNumber=` : the commit number in the branch otherwise 1 on a tag
* `commitSha1=` : the commit ID
* `dateTime=` : the date time in UTC format when the packaging is done

:::{tip}
These extra parameters are specific to QGIS Plugin CI, so it's strongly recommended storing them below a dedicated section:

```ini
[tool:qgis-plugin-ci]
commitNumber=
commitSha1=
dateTime=
```

:::
