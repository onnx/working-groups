# ==========================================================
# Makefile pour la vérification formelle de l'opération 'CONV'
# Ce Makefile est exécuté depuis : ops/spec/formal/CONV/
# ==========================================================

.PHONY: prove update clean
#Directories 
DOC_DIR = generated_doc
CODE_DIR = generated_code


# ==========================================================
# CIBLES
# ==========================================================

# --- Vérification des preuves ---
prove:
	@echo "------------------------------------------"
	@echo "--- Proofs for 'Dequantize Linear' operation"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l -s -x

# --- Mise à jour des sessions Why3 ---
update:
	@echo "------------------------------------------"
	@echo "--- Update Proofs for 'Dequantize Linear'"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l -s -x -m

doc:
	@echo "------------------------------------------"
	@echo "--- Documentation"
	@echo "------------------------------------------"
	@rm -fr html
	@why3find doc *.mlw -t "Dequantize Linear operator" -o $(DOC_DIR)
EXTRACT = -D c -D cdriver.drv -L . --modular --interface -o $(CODE_DIR) 

lib:
	@echo "------------------------------------------"
	@echo "--- Extraction"
	@echo "------------------------------------------"
	@rm -fr $(CODE_DIR)
	@why3 extract $(EXTRACT) \
	    tensor.libvector.CIndex \
	    tensor.libtensor.CTensor \
	    libtensor.CTensorInt32 \
	    libtensor.CTensorDequantizeLinear
	@cd $(CODE_DIR) && gcc -c *.c
	@find $(CODE_DIR) -type f | sort
	@cd $(CODE_DIR) && gcc -c *.c
	@find $(CODE_DIR) -type f | sort

# --- Nettoyage des fichiers générés ---
clean:
	rm -f $(CODE_DIR)
	rm -f $(DOC_DIR)
