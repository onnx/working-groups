# ==========================================================
# Makefile pour la vérification formelle de l'opération 'relu'
# Ce Makefile est exécuté depuis : ops/spec/formal/relu/
# ==========================================================

.PHONY: prove update clean
#Directories 
DOC_DIR = ../../../code/relu/generated_doc
CODE_DIR = ../../../code/relu/generated_code/c_code
CDRIVER_DIR = ../common/drivers
LIBTENSOR_DRIVER_DIR = ../common/drivers
SRC_TENSOR = ../common/libs/tensor


# ==========================================================
# CIBLES
# ==========================================================

# --- Vérification des preuves ---
prove:
	@echo "------------------------------------------"
	@echo "--- Proofs for 'relu' operation"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l -s -x

# --- Mise à jour des sessions Why3 ---
update:
	@echo "------------------------------------------"
	@echo "--- Update Proofs for 'relu'"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l -s -x -m

doc:
	@echo "------------------------------------------"
	@echo "--- Documentation"
	@echo "------------------------------------------"
	@rm -fr html
	@why3find doc *.mlw -t "relu operator" -o $(DOC_DIR)
EXTRACT_LIB = -D c -D $(CDRIVER_DIR)/cdriver.drv -L $(SRC_TENSOR) --modular --interface -o $(CODE_DIR) 
EXTRACT_RELU = -D c -D relu_driver.drv -D $(LIBTENSOR_DRIVER_DIR)/libtensor.drv -L . --modular --interface -o $(CODE_DIR)

lib:
	@echo "------------------------------------------"
	@echo "--- Extraction"
	@echo "------------------------------------------"
	@rm -fr $(CODE_DIR)
	@why3 extract $(EXTRACT_LIB) tensor.libtensor.CTensor
	@why3 extract $(EXTRACT_LIB) tensor.libvector.CIndex
	@why3 extract $(EXTRACT_RELU) relu.CTensorReLU
	@cd $(CODE_DIR) && gcc -c *.c
	@find $(CODE_DIR) -type f | sort

# --- Nettoyage des fichiers générés ---
clean:
	rm -f $(CODE_DIR)
	rm -f $(DOC_DIR)
