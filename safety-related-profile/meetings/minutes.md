# 2024/11/06
## Agenda (proposal)
(Floating point numbers)
In the last meeting, we have identified that the precision (of computations) of computations are issue. This subject deserves a dedicated meeting and work. All material concerning this topics can be found [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues). A first list of questions and some "food for thought" are available [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md)

# 2024/10/23
## Agenda
- Review of actions
- Rapid review of current contents of Use Cases and Needs
- Work sharing and commitments (who can contribute to what?)
- Work on the PoC : review of the informal description, improvements
- Other events
## Participants

JENN Eric, TURKI Mariem, Filipo PEROTTO, Julien VIDALIE, Andreas Fehlner, JB Rouffet, BELCAID Mohammed, Nicolas Valot, BELFY Henri, Luís Conde, BONNAFOUS Eric, Jean-Loup Farges, Jean Souyris, 
Cong Liu, Dumitru Potop, Claire Pagetti, Edoardo Manino, Boblest Sebastian 

## Minutes
- Presentation of the Use Case document
  - Airbus Aircraft (target DAL C), Thales AVS (29-32 : not necessary, DAL : not yet defined, MobileNet and YoloV8 are necessary)
          - Dumitru would be interrested in having a presentation of the Use case? In particular what are the use cases using recurrent networks... (no action at this point)
          - Jean: there are significant differences between the operator sets. In fact, THAV has listed the operators from the standard models (e.g., Yolo) they plan to use.
  - Classification of operators
      - Nicolas proposes a tentative classification (see [here]([to be defined](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/ONNX_Op_classification.xlsx))).
          - [ ] (All) Check Nicolas' classification proposal 
      - [ ] (Mohammed) Propose a use case for CS, [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
      - Jean-Loup proposes to add a classification criterion concerning certification in order to group operators raising similar issues. (Sebastian: e.g. operators potentially raising to numerical exceptions...)
      - [ ] (Jean-Baptiste) Provide a first analysis of the ARP 6983 / EASA concept paper
      - Sebastian: Customers often develop their model from scratch for they have very specific needs. They usually don't use models out of a zoo. For quantified model, they use TensorFlow lite. They are not using quantified ONNX quentified operators.
      - [ ] (Sebastian) Get in touch with other people in the automotive partners (e.g. ETAS).
- Review of the PoC specification
  - [ ] (Sebastian and Luis) Review of the [Conv2d operator](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example).
  - [ ] (Luis) Provide contact(s) with medical domain
- Claire and Christophe to make a presentation to [ISCLP ](https://www.defense.gouv.fr/dga/evenements/ouverture-inscriptions-au-seminaire-futur-lembarque-critique-systemes-combat) about ARP, replication, etc.
- [ ] (Eric) Provide one slide about SONNX.
- Eric and Jean will discuss with people from the [DeepGreen](https://deepgreen.ai/) project in order to see how we coud share the effort / reference implementation
- **/!\PLEASE CONTRIBUTE TO THE DESCRIPTION OF [USE CASES](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md) AND [NEEDS/REQS](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/needs.md) /!\\**
  - Concerning use cases, please provide links to the standard models (when applicable)

#### New actions
- [ ] (231001 - All) Check Nicolas' classification proposal 
- [ ] (231002 - Mohammed) Propose a use case for CS, [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
- [ ] (231002 - Jean-Baptiste) Provide a first analysis of the ARP 6983 / EASA concept paper
- [ ] (231002 - Sebastian) Get in touch with other people in the automotive partners (e.g. ETAS).
- [ ] (231002 - Sebastian and Luis) Review of the [Conv2d operator](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example).
- [ ] (231002 - Luis) Provide contact(s) with other industrial domains (medical,...)
- [ ] (231002 - Eric) Provide one slide about SONNX.


#### Previous actions
- [ ] (A008 - leads) Plan SC meetings
      - No action.
- [ ] (A009 - Dumitru) Correct  / complete description of issue #2
- [X] (A010 - leads) Create a “tools” area <closed on 03/10>
- [X] (A011 - Nicolas) Deposit his operator extraction tool in the repository. <closed on 03/10>
- [X] (A012 - Nicolas) Review the the "issues" document
      - Pending
- [ ] (A013 - leads) Organize a meeting on numerical computations (fp-sg)
      - Pending. Subject to be addressed durint the next meeting 2024/11/06. Draft material is available [here]{https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md}. Please add your ideas / remarks...
- [ ] (A014 - fp-sg) Provide a clear statement of the numerical computations issues.
      - See A013.
- [ ] (A015) All : Complete description of use cases
      - Pending
- [ ] (A016) All : Complete description of needs
      - Pending
- [ ] (A002 - all) Add / remove your name for the [participant list ](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/team.md) and provide information about your possible contribution
- [ ] (A004 - all) Propose a short communication during the next WG meetings. The list is [here](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/presentation_proposals.md).
      - Sebastian Boblest (Bosch), on their tool (to be planned)
      - Alexandre Eichenberger (IBM),  on onnx-mlir (to be planned)
      - ??? on specification and verification of FP computations
- [X] (A005 - leads) Organize sub-group on formal methods (fm-sg).
      => Meeting planned on 29/10
- [ ] (A006 - leads) Finalize the organization of the WG's repository. Define procedure to use it (inc. issues, wiki,...)
      - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
- [ ] (A007 - leads) Setup a mailing list
      - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
# 2024/10/02
## Agenda
- Presentation of "templates" to start of activies on
    - definition of [use cases, models, operators](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
    - elicitation of [needs](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/needs.md)
    - identificaiton of [issues ](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/issues.md)
- Discussion about the creation of a sub-group (who?)
    - on formal methods
    - on numerical issues (?)
- Status of integration with ONNX community
    - Brief presentation of the Linux Fundation support to our activities (=> Andreas, Friday, report during next meeting)
  
## Participants
(Was not able to retrieve the list from TEAMS)
## Minutes
- See agenda
  
### About the “Steering Committee”
- EMB will not be able to participate to our periodic meetings (every two weeks) but is nevertheless willing to contribute to our effort via a *Streeing Committe* (SC). The objective of the SC is to monitor important (”key”) moments in the progression of activities (“gates” , “phase transitions”, etc.).
- The SC shall be planned in advance. Basically: one SC every SC will be fine.
- [ ] (A008 - leads) Plan SC meetings

### About the templates
3 “template” document were presented (see link above)
- “Issues template”
    - Dumitru proposes to add a description / illustration of the effects of an issue. ⇒ to be added in the template
    - Concerning issue #2 (order of operations)
        - Dumitru (following a remark already done by Sebastian, a long time ago…)  emphasizes that there is not problem of non determinism / interpretation on the order of processing of operator: if one follows the topological ordering,  result of floating point computations are completely and unambiguoulsy determined. There may still be issues with random numbers.
        - [ ]  (A009 - Dumitru) Correct  / complete description of issue #2
- Use case / scope template
    - Nicolas : a description can simply refer to an existing model in the Hugging Face repository using a hypertext link.
    - Nicolas proposes a script to extract the list of operators. (To be placed in the “tools” area)...
    - [ ] (A010 - leads) Create a “tools” area
    - [ ] (A011 - Nicolas) Deposit his operator extraction tool in the repository
    - [ ] (A012 - Nicolas) Review the the "issues" document
  
### About sub-groups

- Floating point computation
    - [ ]  (A013 - leads) Organize a meeting on numerical computations (fp-sg)
    - [ ]  (A014 - fp-sg) Provide a clear statement of the numerical computations issues.

- Formal methods
    - The PoC must be completed, incl. aspect about formal methods
    - The value of a formal specification must be estimated (value in terms of communication, automation,…)
    - A formal language must be selected.
    - This is to be covered by the fm-sg, see action A005

Other (off-meeting) 
- [ ]  (Nicolas) See if we can involve the authors of the paper on ONNX conversion in order to identify Exploiter le papier / probblème
      
#### New actions
- [ ] (A008 - leads) Plan SC meetings
- [ ] (A009 - Dumitru) Correct  / complete description of issue #2
- [X] (A010 - leads) Create a “tools” area <closed on 03/10>
- [X] (A011 - Nicolas) Deposit his operator extraction tool in the repository. <closed on 03/10>
- [ ] (A012 - Nicolas) Review the the "issues" document
- [ ] (A013 - leads) Organize a meeting on numerical computations (fp-sg)
- [ ] (A014 - fp-sg) Provide a clear statement of the numerical computations issues.
- [ ] (A015) All : Complete description of use cases
- [ ] (A016) All : Complete description of needs

#### Previous actions
- [X] (A001 - Embraer) Clarify the role / organisation of the "Steering Committe". <closed on 02/10>
- [ ] (A002 - all) Add / remove your name for the [participant list ](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/team.md) and provide information about your possible contribution
- [X] (A003 - leads) Create templates to start feeding the list of **use cases**, **needs**, **requirements**, **issues**. <closed on 02/10>
- [ ] (A004 - all) Propose a short communication during the next WG meetings. The list is [here](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/presentation_proposals.md).
- [ ] (A005 - leads) Organize sub-group on formal methods (fm-sg).
- [ ] (A006 - leads) Finalize the organization of the WG's repository. Define procedure to use it (inc. issues, wiki,...)
- [ ] (A007 - leads) Setup a mailing list

#### Closed actions
(to be completed)
