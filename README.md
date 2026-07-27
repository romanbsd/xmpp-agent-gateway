# XMPP Agent Gateway ProtoXEP

This repository contains a proposed XMPP Extension Protocol for hosting,
discovering, searching, and invoking addressable AI agents and their tools over
XMPP.

The specification grew out of real-world multi-agent orchestration work using
Openfire. It defines:

- stable agent identities based on bare JIDs;
- gateway and endpoint discovery using XMPP service discovery;
- directory browsing and search;
- versioned agent manifests and separately retrievable JSON Schemas;
- asynchronous tool invocation with acceptance, progress, interactive input,
  cancellation, terminal results, and task recovery;
- mapping between XMPP tools and Model Context Protocol tool objects;
- hosting, authorization, federation, privacy, and security requirements; and
- ordinary human-to-agent messaging alongside task execution.

The document is currently a **ProtoXEP**. It has not yet been accepted or
approved by the XMPP Standards Foundation.

## Files

- `protoxep-xmpp-agent-gateway.xml` — authoritative ProtoXEP source.
- `protoxep-xmpp-agent-gateway.html` — generated review copy.
- `validate.py` — embedded example, schema, and artifact-hash validator.
- `xep.dtd`, `xep.ent`, and `xep.xsl` — XSF document tooling.
- `xmpp.css`, `prettify.css`, and `prettify.js` — generated-document assets.
- `Makefile` — validation and HTML/PDF rendering commands.

## Requirements

Install Python 3, `libxml2`, and `libxslt`. The latter two provide `xmllint`
and `xsltproc`.

On macOS with Homebrew:

```sh
brew install libxml2 libxslt
```

## Validate

Run all validation checks:

```sh
make lint
```

This validates the document against the bundled XEP DTD, parses every embedded
XML example, checks the syntax of normative JSON Schemas, compiles the embedded
XML Schemas against representative payloads, and verifies canonical artifact
hashes. The Python validator uses only the standard library and `xmllint`.

## Render HTML

Run:

```sh
make html
```

This is equivalent to:

```sh
xsltproc xep.xsl protoxep-xmpp-agent-gateway.xml \
  > protoxep-xmpp-agent-gateway.html
```

Open `protoxep-xmpp-agent-gateway.html` in a browser to review the rendered
specification.

## Editing

Edit the XML source rather than the generated HTML. Before submitting changes:

```sh
make lint
make html
git diff --check
```

Commit the regenerated HTML together with XML changes so reviewers can inspect
the specification without installing the XSF toolchain.

## Author

Roman Shterenzon  
<roman.shterenzon@gmail.com>
