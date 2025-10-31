# ==========================================================
# Makefile pour la vérification formelle de l'opération 'where'
# Ce Makefile est exécuté depuis : ops/spec/formal/where/
# ==========================================================

.PHONY: prove update clean
#Directories 
DOC_DIR = ../../../code/where/generated_doc
CODE_DIR = ../../../code/where/generated_code/c_code
CDRIVER_DIR = ../../../code/common/drivers

# ==========================================================
# CIBLES
# ==========================================================

# --- Vérification des preuves ---
prove:
	@echo "------------------------------------------"
	@echo "--- Proofs for 'where' operation"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l -s -x

# --- Mise à jour des sessions Why3 ---
update:
	@echo "------------------------------------------"
	@echo "--- Update Proofs for 'where'"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l -s -x -m

doc:
	@echo "------------------------------------------"
	@echo "--- Documentation"
	@echo "------------------------------------------"
	@rm -fr html
	@why3find doc *.mlw -t "Where operator" -o $(DOC_DIR)
EXTRACT=-D c -D where_driver.drv -L . --modular --interface -o $(CODE_DIR)

lib:
	@echo "------------------------------------------"
	@echo "--- Extraction"
	@echo "------------------------------------------"
	@rm -fr $(CODE_DIR)
	@why3 extract $(EXTRACT) where.CTensorWhere
	@cd $(CODE_DIR) && gcc -c *.c
	@find $(CODE_DIR) -type f | sort

# --- Nettoyage des fichiers générés ---
clean:
	rm -f $(CODE_DIR)
	rm -f $(DOC_DIR)
