# Recording and Transcript:

https://zoom.us/rec/share/TuRGpiOMpQoOFUYR_4W52shLn9su8HkKyuF_TkFCjJJ0Q_robuYGCoSmXVw9E8EK.H3rppgZPDEBz-P8V

# Meeting Minutes:

## Presentation Review & Status Updates: 
- Yamini Nimmagadda shared a [presentation](https://docs.google.com/presentation/d/1FlEZmvLrgFcnkv4ScEWHOAzKXyp977vH) detailing updates for the working group's scope to prepare for the ONNX Meetup. Some of the changes/updates include:
  - Updating Linear Attention to the merged category as it is expected in the upcoming release candidate.
  - The proposal for GroupMatMul is in progress. Seeking input from IHVs and community for definition
  - Yamini noted that Ternary Storage Format & 2-Bit Quantization has not yet been merged. She will follow up with Soumendu regarding the submission of the RFC.
  - Paged Attention remains a tentative, proposed topic requiring further development. The group discussed whether it requires framework-level standardization (e.g., handling KVCache, block IDs, page tables) or remains purely a backend implementation strategy.
  - Rama mentioned about an active [backend implementation](https://github.com/onnx/onnx/issues/7494#issuecomment-4554027526) proposal for Flex Attention and will look into a recently submitted prototype/reference implementation from the original PR author.

## Exporters & Backend Context 
- Hugging Face (HF) Exporters & optimum-onnx: The team discussed about the open [PR](https://github.com/huggingface/transformers/pull/41992) for HF exporters. The path forward involves utilizing HF exporters directly within Optimum ONNX to streamline exporting transformer models.
- Backend Context & Ahead-of-Time (AOT): Javier summarized high-level progress on the base RFC, focusing on packaging, validation strings before downloading/loading, and integrating weight reuse features to manage package sizing.

## Working Group Logistics & Meeting Cadence
- Cadence Change: The working group agreed to shift from a bi-weekly to a monthly meeting cadence through the end of the year to maintain focused progress on ongoing topics like backend context and HF exporters.
- The group will begin setting and announcing clear meeting agendas ahead of time so stakeholders can selectively attend relevant discussions.
- ONNX Meetup Presentation: Rama will present this working group update at the upcoming ONNX meetup, as Yamini and Javier will be out of office.
- Next Meeting: Because Yamini is out of the office for the next five weeks, the group will bypass meetings prior to the meetup and officially reschedule for mid July. Ongoing collaboration will continue over Slack.
