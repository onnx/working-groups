# ==========================================================
# Makefile pour la vérification formelle de l'opération 'leakyrelu'
# Ce Makefile est exécuté depuis : ops/spec/formal/leakyrelu/
# ==========================================================

.PHONY: prove update clean
#Directories 
DOC_DIR = ../../../code/leakyrelu/generated_doc
CODE_DIR = ../../../code/leakyrelu/generated_code/c_code
CDRIVER_DIR = ../common/drivers
LIBTENSOR_DRIVER_DIR = ../common/drivers
SRC_TENSOR = ../common/libs/tensor


# ==========================================================
# CIBLES
# ==========================================================

# --- Vérification des preuves ---
prove:
	@echo "------------------------------------------"
	@echo "--- Proofs for 'leakyrelu' operation"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l -s -x

# --- Mise à jour des sessions Why3 ---
update:
	@echo "------------------------------------------"
	@echo "--- Update Proofs for 'leakyrelu'"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l -s -x -m

doc:
	@echo "------------------------------------------"
	@echo "--- Documentation"
	@echo "------------------------------------------"
	@rm -fr html
	@why3find doc *.mlw -t "leakyrelu operator" -o $(DOC_DIR)
EXTRACT_LIB = -D c -D $(CDRIVER_DIR)/cdriver.drv -L $(SRC_TENSOR) --modular --interface -o $(CODE_DIR) 
EXTRACT_LEAKYRELU = -D c -D leakyrelu_driver.drv -D $(LIBTENSOR_DRIVER_DIR)/libtensor.drv -L . --modular --interface -o $(CODE_DIR)

lib:
	@echo "------------------------------------------"
	@echo "--- Extraction"
	@echo "------------------------------------------"
	@rm -fr $(CODE_DIR)
	@why3 extract $(EXTRACT_LIB) tensor.libtensor.CTensor
	@why3 extract $(EXTRACT_LIB) tensor.libvector.CIndex
	@why3 extract $(EXTRACT_LEAKYRELU) leakyrelu.CtensorLeakyRelu
	@cd $(CODE_DIR) && gcc -c *.c
	@find $(CODE_DIR) -type f | sort

# --- Nettoyage des fichiers générés ---
clean:
	rm -f $(CODE_DIR)
	rm -f $(DOC_DIR)
