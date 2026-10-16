.RECIPEPREFIX := >

# ==========================================================
# Makefile pour ArgMax
# - preuve de la spécification abstraite
# - extraction C du kernel concret CtensorArgMax
# ==========================================================

.PHONY: prove prove_all update doc lib show grep clean veryclean spec_only

DOC_DIR = ./argmax_generated/doc
CODE_DIR = ./argmax_generated/c_code

CDRIVER_DIR = $(HOME)/working-groups/safety-related-profile/sonnx/ops/spec/formal/common/drivers
LIBTENSOR_DRIVER_DIR = $(HOME)/working-groups/safety-related-profile/sonnx/ops/spec/formal/common/drivers
SRC_TENSOR = $(HOME)/working-groups/safety-related-profile/sonnx/ops/spec/formal/common/libs/tensor

SRC = argmax.mlw
SPEC_ONLY = argmax_spec_only.mlw

EXTRACT_LIB = -D c -D $(CDRIVER_DIR)/cdriver.drv -L $(SRC_TENSOR) --modular --interface -o $(CODE_DIR)
EXTRACT_ARGMAX = -D c -D argmax_driver.drv -D $(LIBTENSOR_DRIVER_DIR)/libtensor.drv -L . -L $(SRC_TENSOR) --modular --interface -o $(CODE_DIR)

spec_only:
> @echo "------------------------------------------"
> @echo "--- Building abstract-only ArgMax file"
> @echo "------------------------------------------"
> @python3 -c 'from pathlib import Path; s=Path("argmax.mlw").read_text(); marker="\nmodule ArgMax_Concrete"; assert marker in s, "module ArgMax_Concrete not found"; Path("argmax_spec_only.mlw").write_text(s.split(marker)[0].rstrip()+"\n"); print("OK: generated argmax_spec_only.mlw")'

prove: spec_only
> @echo "------------------------------------------"
> @echo "--- Proofs for abstract ArgMax specification"
> @echo "------------------------------------------"
> @why3find prove $(SPEC_ONLY) -l -s -x

prove_all:
> @echo "------------------------------------------"
> @echo "--- Proofs for all ArgMax theories"
> @echo "------------------------------------------"
> @why3find prove $(SRC) -l -s -x

update: spec_only
> @echo "------------------------------------------"
> @echo "--- Update Proofs for abstract ArgMax"
> @echo "------------------------------------------"
> @why3find prove $(SPEC_ONLY) -l -s -x -m

doc: spec_only
> @echo "------------------------------------------"
> @echo "--- Documentation"
> @echo "------------------------------------------"
> @rm -rf $(DOC_DIR)
> @mkdir -p $(DOC_DIR)
> @why3find doc $(SPEC_ONLY) -t "ArgMax operator" -o $(DOC_DIR)

lib:
> @echo "------------------------------------------"
> @echo "--- Extraction"
> @echo "------------------------------------------"
> @rm -rf $(CODE_DIR)
> @mkdir -p $(CODE_DIR)
> @why3 extract $(EXTRACT_LIB) tensor.libtensor.CTensor
> @why3 extract $(EXTRACT_LIB) tensor.libvector.CIndex
> @why3 extract $(EXTRACT_ARGMAX) argmax.ArgMax_Concrete
> @python3 patch_argmax_c.py
> @echo "------------------------------------------"
> @echo "--- C compilation"
> @echo "------------------------------------------"
> @cd $(CODE_DIR) && gcc -c *.c -lm
> @echo "------------------------------------------"
> @echo "--- Generated files"
> @echo "------------------------------------------"
> @find $(CODE_DIR) -type f | sort

show:
> @echo "------------------------------------------"
> @echo "--- Generated files"
> @echo "------------------------------------------"
> @find $(CODE_DIR) -type f | sort

grep:
> @echo "------------------------------------------"
> @echo "--- Search ArgMax symbols"
> @echo "------------------------------------------"
> @grep -R "c_argmax\\|argmax\\|isnan\\|isgreater" -n $(CODE_DIR) || true

clean:
> @rm -rf $(CODE_DIR)
> @rm -rf $(DOC_DIR)
> @rm -f $(SPEC_ONLY)

veryclean:
> @rm -rf argmax_generated html
> @rm -f $(SPEC_ONLY)
