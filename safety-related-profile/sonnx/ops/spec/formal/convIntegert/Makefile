# ==========================================================
# Makefile pour la vérification formelle de l'opération 'leakyrelu'
# Ce Makefile est exécuté depuis : ops/spec/formal/leakyrelu/
# ==========================================================

.PHONY: prove update clean
#Directories 
DOC_DIR = ../../../code/convInteger/generated_doc
CODE_DIR = ../../../code/convInteger/generated_code/c_code
CDRIVER_DIR = ../common/drivers
LIBTENSOR_DRIVER_DIR = ../common/drivers
SRC_TENSOR = ../common/libs/tensor
SRC_TENSORINT = ../common/libs/tensorint


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
EXTRACT_LIB_INT =  -D c -D $(CDRIVER_DIR)/tensorint.drv -L $(SRC_TENSORINT) --modular --interface -o $(CODE_DIR)
EXTRACT_CONV = -D c -D convInteger_driver.drv -L . --modular --interface -o $(CODE_DIR)

lib:
	@echo "------------------------------------------"
	@echo "--- Extraction"
	@echo "------------------------------------------"
	@rm -fr $(CODE_DIR)
	@why3 extract $(EXTRACT_LIB) tensor.libvector.CIndex
	@why3 extract $(EXTRACT_LIB_INT) tensorint.ctensorint8.CTensorInt8
	@why3 extract $(EXTRACT_LIB_INT) tensorint.libtensor.CTensorUInt8
	@why3 extract $(EXTRACT_LIB_INT) tensorint.libtensor.CTensorInt32
	@why3 extract $(EXTRACT_LIB_INT) tensorint.libtensor.CTensorUInt32
	@why3 extract $(EXTRACT_CONV) copconvinteger.COPConvInteger
	@cd $(CODE_DIR) && gcc -c *.c
	@find $(CODE_DIR) -type f | sort

# --- Nettoyage des fichiers générés ---
clean:
	rm -f $(CODE_DIR)
	rm -f $(DOC_DIR)
