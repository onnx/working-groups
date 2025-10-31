# Meeting 03-07-2025 10:00

Attendees: nicolas.valot@airbus.com,  Sebastian.Boblest@de.bosch.com, Valentin.Poirot@de.bosch.com

1. To specify that seq_length, batch_size, input_size shall be constant values (linked to tensor dimensions)

2. We should not be restrictive so that the profile will raise some interest in the ONNX community.
I will remove restrictions on initial conditions, peephole.
We agreed that sequence_lens might be used only when batch_size is > 1, but appears to be exotic.
B (bias) is not optional and shall be defined to 0..0 when unused to respect the 'unambiguous / explicit' requirements.

3. This raises the need of :
a tool to convert ONNX to SONNX (to convert implicit attributes to explicit ones, to add reshape upon broadcast ...)
a tool to verify SONNX profile (extension of the existing ONNX checker ?)
Comments:
Bosh says it is urgent to propose and commit with ONNX that the SONNX profile will become mainstream.
To push into this direction, we need a clever way to specify the operators, so that our specification complies with ONNX without any restriction.

I propose that for each operator .md file, we specify the full compliance with ONNX spec and we add a bottom section SONNX in the operator page, where we express the restrictions like : this input XXX shall be static, the B bias shall be explicitly defined, Broadcast not supported (reshape shall be prepended when required)...

This will show our specification work (math expressions, illustrations) mainstream to all the ONNX community from the ONNX documentation entry point, and also the SONNX 'value' for curious/interested  people at the bottom of each operator page.

For visibility and adoption, we shall avoid having a SONNX documentation entry point different from mainstream ONNX.

I will try to reorganize the lstm.md file in this manner to see what it looks like.

We shall trace our modifications in the lstm/review folder (to be created).