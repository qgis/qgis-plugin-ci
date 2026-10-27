# Skipping security rules

Every plugin and plugin version uploaded to [the QGIS Plugins Website](https://plugins.qgis.org/) is automatically scanned for security Issues. All details on this process can be found on the [Security Scanning site](https://plugins.qgis.org/docs/security-scanning).

When authenticating using `--osgeo-username` and `--osgeo-password`, security rules are [always skipped](https://plugins.qgis.org/docs/security-scanning/skipping)

When authenticating using `--qgis-token`, you may configure security rules to be skipped using the `skip_security_rules` key.

The value is a list of all security rules you want to skip, identified by their precise rule check code as shown on the [Security Rules reference page](https://plugins.qgis.org/docs/security-scanning/rules).

## Examples

### Using YAML file `.qgis-plugin-ci`

```yaml
skip_security_rules:
  - B311
  - KeywordDetector
```

### Using INI file `setup.cfg`

```ini
[qgis-plugin-ci]
skip_security_rules =
    B311
    KeywordDetector
```

### Using TOML file `pyproject.toml`

```toml
[tool.qgis-plugin-ci]
skip_security_rules = [
    "B311",
    "KeywordDetector",
]
```
