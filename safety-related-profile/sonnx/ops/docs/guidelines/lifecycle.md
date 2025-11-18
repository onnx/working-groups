The lifecycle of the informal specification, formal specification, and tests item is managed using Github's [SONNX project](https://github.com/users/ericjenn/projects/4)

- I you don't have write access, please ask Eric.

- If you start working on a new operator, create an item in the "Dev in progress" column. 
	- Use the following conventions (replace "informal" by "formal" or "test" depending on the item).
	- Use 
    	- Title: Informal space "<your operator>"
    	- Description: Develop informal specification of operator [<your operator>](https://onnx.ai/onnx/operators/onnx__<your operator>.html) 
	- Assign it to you
	- Set the label to "Informal", "Formal" or "Test" in order to facilitate filtering.
- Then, move the item to the appropriate column depending on its state.:
	- Dev in progress: (the spec / code / ...) is being developed 
	- Ready for review: the item has been created and is ready to be reviewed 
	- Review in progress: the item is being reviewed
	- Review complete: the item has been reviewed, it is ready for corrections
	- Correction in progress: the item is being corrected. Once corrected, it moves either to "Completed" if no new review is necessary or to "Ready for review" if a new review is necessary.
	- Corrections completed: the item has been corrected according to the review. Reviewers can chek that the corrections have been correctly taken into account. Once OK, the item moves to "completed".
	- Completed

- Items in the kanban are reviewed during the SONNX meetings.
- Use the Github's "Comment" to make your comments (preferably), or create a file "<my_name>.md" in a "Reviews" folder of the directory corresponding to the operator (see [here](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/add) for the add operator). 
