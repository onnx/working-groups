#pragma once

#include <string>
#include <set>

namespace onnx::genai {

struct GenerationConfig
{
    // The maximum length the generated tokens can have
    // (input_tokens + output_tokens)
    size_t max_length = SIZE_MAX;

    // The maximum number of tokens to generate
    // (not including input tokens)
    size_t max_new_tokens = SIZE_MAX;

    // The minimum numbers of tokens to generate,
    // (not including input tokens)
    size_t min_new_tokens = 0;

    // The ids of the end-of-sequence tokens to use.
    std::set<int64_t> eos_token_ids;

    // a list of strings that should terminate generation if the model outputs them.
    std::set<std::string> stop_strings;

    struct SamplingConfig
    {
        // Whether or not to use sampling; use greedy decoding otherwise.
        bool do_sample = false;

        //
        // The following parameters are only applicable if do_sample = true.
        //

        // Seed used for RNG (Random Number Generator).
        size_t rng_seed = 0;

        // The value used to module the next token probabilities
        float temperature = 1.0f;

        // The number of highest probability vocabulary tokens to keep for top-k-filtering
        size_t top_k = std::numeric_limits<size_t>::max();

        // If set to float < 1, only the smallest set of most probable tokens with
        // probabilities that add up to top_p or higher are kept for generation.
        float top_p = 1.0f;

        // The parameter for repetition penalty. 1.0 means no penalty.
        // See [https://huggingface.co/papers/1909.05858] for more details.
        // // Only applicable if do_sample=true.
        float repetition_penalty = 1.0f;
    };

    SamplingConfig sampling_config;

    struct BeamSearchConfig
    {
        // Number of beams for beam search.  1 means no beam search.
        size_t num_beams = 1;

        //
        // The following parameters are only applicable if num_beams > 1.
        //

        // Number of groups to divide num_beams into in order to ensure diversity
        // among different groups of beams.
        size_t num_beam_groups = 1;

        // This value is subtracted from a beam’s score if it generates a token same
        // as any beam from other group at a particular time.
        float diversity_penalty = 0.0f;

        // Exponential penalty to the length that is used with beam-based generation.
        // It is applied as an exponent to the sequence length, which in turn is used
        // to divide the score of the sequence. Since the score is the log likelihood
        // of the sequence (i.e. negative), length_penalty > 0.0 promotes longer sequences,
        // while length_penalty < 0.0 encourages shorter sequences.
        float length_penalty = 1.0f;

        // The number of independently computed returned sequences for each element
        // in the batch.
        size_t num_return_sequences = 1;

        // If set to int > 0, all ngrams of that size can only occur once
        size_t no_repeat_ngram_size = std::numeric_limits<size_t>::max();
        /**
         * @brief controls the stopping condition for grouped beam search.
         *        The following values are possible:
         *        "EARLY" stops as soon as there are `num_beams` complete candidates.
                  "HEURISTIC" stops when is it unlikely to find better candidates.
                  "NEVER" stops when there cannot be better candidates.
         */
        enum class StopCriteria { EARLY, HEURISTIC, NEVER };

        StopCriteria stop_criteria = StopCriteria::HEURISTIC;
    };

    BeamSearchConfig beam_search_config;
};

} // namespace onnx::genai
