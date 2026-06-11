.RECIPEPREFIX := >

# ==========================================================
# Makefile pour Softmax
# - preuve de la spécification abstraite
# - extraction C du kernel concret CtensorSoftmax
# ==========================================================

.PHONY: prove prove_all update doc lib show grep clean veryclean spec_only

DOC_DIR = ./softmax_generated/doc
CODE_DIR = ./softmax_generated/c_code

CDRIVER_DIR = $(HOME)/working-groups/safety-related-profile/sonnx/ops/spec/formal/common/drivers
LIBTENSOR_DRIVER_DIR = $(HOME)/working-groups/safety-related-profile/sonnx/ops/spec/formal/common/drivers
SRC_TENSOR = $(HOME)/working-groups/safety-related-profile/sonnx/ops/spec/formal/common/libs/tensor

SRC = softmax.mlw
SPEC_ONLY = softmax_spec_only.mlw

EXTRACT_LIB = -D c -D $(CDRIVER_DIR)/cdriver.drv -L $(SRC_TENSOR) --modular --interface -o $(CODE_DIR)
EXTRACT_SOFTMAX = -D c -D softmax_driver.drv -D $(LIBTENSOR_DRIVER_DIR)/libtensor.drv -L . -L $(SRC_TENSOR) --modular --interface -o $(CODE_DIR)

spec_only:
> @echo "------------------------------------------"
> @echo "--- Building abstract-only Softmax file"
> @echo "------------------------------------------"
> @python3 -c 'from pathlib import Path; s=Path("softmax.mlw").read_text(); marker="\nmodule CtensorSoftmax"; assert marker in s, "module CtensorSoftmax not found"; Path("softmax_spec_only.mlw").write_text(s.split(marker)[0].rstrip()+"\n"); print("OK: generated softmax_spec_only.mlw")'

prove: spec_only
> @echo "------------------------------------------"
> @echo "--- Proofs for abstract Softmax specification"
> @echo "------------------------------------------"
> @why3find prove $(SPEC_ONLY) -l -s -x

prove_all:
> @echo "------------------------------------------"
> @echo "--- Proofs for all Softmax theories"
> @echo "------------------------------------------"
> @why3find prove $(SRC) -l -s -x

update: spec_only
> @echo "------------------------------------------"
> @echo "--- Update Proofs for abstract Softmax"
> @echo "------------------------------------------"
> @why3find prove $(SPEC_ONLY) -l -s -x -m

doc: spec_only
> @echo "------------------------------------------"
> @echo "--- Documentation"
> @echo "------------------------------------------"
> @rm -rf $(DOC_DIR)
> @mkdir -p $(DOC_DIR)
> @why3find doc $(SPEC_ONLY) -t "Softmax operator" -o $(DOC_DIR)

lib:
> @echo "------------------------------------------"
> @echo "--- Extraction"
> @echo "------------------------------------------"
> @rm -rf $(CODE_DIR)
> @mkdir -p $(CODE_DIR)
> @why3 extract $(EXTRACT_LIB) tensor.libtensor.CTensor
> @why3 extract $(EXTRACT_LIB) tensor.libvector.CIndex
> @why3 extract $(EXTRACT_SOFTMAX) softmax.CtensorSoftmax
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
> @echo "--- Search Softmax symbols"
> @echo "------------------------------------------"
> @grep -R "c_softmax\|c_exp\|exp" -n $(CODE_DIR) || true

clean:
> @rm -rf $(CODE_DIR)
> @rm -rf $(DOC_DIR)
> @rm -f $(SPEC_ONLY)

veryclean:
> @rm -rf softmax_generated html
> @rm -f $(SPEC_ONLY)
