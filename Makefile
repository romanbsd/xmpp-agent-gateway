XML := protoxep-xmpp-agent-gateway.xml
HTML := protoxep-xmpp-agent-gateway.html
PDF := protoxep-xmpp-agent-gateway.pdf
VALIDATOR := validate.py
PYTHON ?= python3
CHROME ?= $(or $(shell command -v google-chrome 2>/dev/null),$(shell command -v chromium 2>/dev/null),$(shell command -v chromium-browser 2>/dev/null),/Applications/Google Chrome.app/Contents/MacOS/Google Chrome)

.PHONY: all lint html pdf presentation

all: lint html

lint: $(XML) $(VALIDATOR)
	xmllint --noout --valid $(XML)
	$(PYTHON) $(VALIDATOR) $(XML)

html: lint
	xsltproc xep.xsl $(XML) > $(HTML)

pdf: html
	"$(CHROME)" --headless --disable-gpu --no-pdf-header-footer \
		--print-to-pdf="$(abspath $(PDF))" "file://$(abspath $(HTML))"

presentation:
	CHROME="$(CHROME)" node presentations/build.mjs
