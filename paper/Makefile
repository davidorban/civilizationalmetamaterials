TEX := civilizational-metamaterials-agi26-r3
REPO := $(shell cd .. && pwd)
PAPER_DIR := $(shell pwd)

.PHONY: paper clean figures arxiv

paper:
	cd $(REPO) && pdflatex -interaction=nonstopmode -output-directory=$(PAPER_DIR) paper/$(TEX).tex
	cd $(REPO) && bibtex $(PAPER_DIR)/$(TEX)
	cd $(REPO) && pdflatex -interaction=nonstopmode -output-directory=$(PAPER_DIR) paper/$(TEX).tex
	cd $(REPO) && pdflatex -interaction=nonstopmode -output-directory=$(PAPER_DIR) paper/$(TEX).tex
	cp $(PAPER_DIR)/$(TEX).pdf $(PAPER_DIR)/preprint/$(TEX).pdf

clean:
	rm -f $(PAPER_DIR)/$(TEX).aux $(PAPER_DIR)/$(TEX).bbl $(PAPER_DIR)/$(TEX).blg \
	       $(PAPER_DIR)/$(TEX).log $(PAPER_DIR)/$(TEX).out $(PAPER_DIR)/$(TEX).pdf

figures:
	cd $(REPO) && python code/figures/fig02_phase_transition.py --out figures/fig02-phase-transition.pdf
	cd $(REPO) && python code/figures/fig05_sensitivity_analysis.py --out figures/fig05-sensitivity-analysis.pdf

arxiv:
	mkdir -p $(PAPER_DIR)/arxiv
	cp $(PAPER_DIR)/$(TEX).tex $(PAPER_DIR)/references-r3.bib \
	   $(PAPER_DIR)/llncs.cls $(PAPER_DIR)/splncs04.bst \
	   $(PAPER_DIR)/arxiv/
	cp -r $(REPO)/figures/fig*.pdf $(PAPER_DIR)/arxiv/
	tar -czf $(PAPER_DIR)/arxiv/$(TEX)-arxiv.tar.gz -C $(PAPER_DIR)/arxiv \
	    $(TEX).tex references-r3.bib llncs.cls splncs04.bst fig*.pdf
	@echo "arXiv tarball: paper/arxiv/$(TEX)-arxiv.tar.gz"
