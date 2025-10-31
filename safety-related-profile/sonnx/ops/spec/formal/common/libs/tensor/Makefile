# Makefile for libvector

.PHONY: all prove update doc lib cc clean
#Directories 
DOC_DIR = ../../../../../code/common/libs/tensor/generated_doc
CODE_DIR = ../../../../../code/common/libs/tensor/generated_code/c_code
CDRIVER_DIR = ../../../../../code/common/drivers

all: prove doc lib
	@echo "------------------------------------------"

prove:
	@echo "------------------------------------------"
	@echo "--- Proofs"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l -s -x

update:
	why3find prove *.mlw -l -s -x -m

doc:
	@echo "------------------------------------------"
	@echo "--- Documentation"
	@echo "------------------------------------------"
	@rm -fr html
	@why3find doc *.mlw -t "Tensor Library" -o $(DOC_DIR)

EXTRACT=-D c -D $(CDRIVER_DIR)/cdriver.drv -L . --modular --interface -o $(CODE_DIR)

lib:
	@echo "------------------------------------------"
	@echo "--- Extraction"
	@echo "------------------------------------------"
	@rm -fr $(CODE_DIR)
	@why3 extract $(EXTRACT) tensor.libvector.CIndex
	@why3 extract $(EXTRACT) tensor.libtensor.CTensor
	@cd $(CODE_DIR) && gcc -c *.c
	@find $(CODE_DIR) -type f | sort

clean:
	rm -fr $(CODE_DIR)
	rm -f $(DOC_DIR)