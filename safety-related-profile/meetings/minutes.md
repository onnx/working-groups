# 2024/11/20

## Agenda
- Review of actions
- Status of deliverables
  - D1.a: Safety-related Profile Scope Definition
  - D1.b.<x>: End users' needs and requirements for domain <x>.
  - D1.c: Consolidated needs for all industrial domains
![image](https://github.com/user-attachments/assets/7b081310-cf71-4136-b796-e254faf72483)
- Discussion about modalities
## Participants
Marko, Sebastian, Julien, Jean, Henri, Augustin, Yohann, Mohammed, Eric B., Eric J.

## Minutes
- We are late: deliverable D1.1 was due Oct. 2024, and D1.2 was due Nov. 2024. We have very few needs / reqs, and all from the aero domain. Additional reqs will certainly come from Jean-Baptiste analysis of Aero standards (see action ). Airbus will propose material to complete the list of needs / reqs by the end of this week.
  - [ ] (Jean, Eric) Integrate Airbus' additional nededs / reqs.
- Providing a first list of needs/reqs will certainly clarify what is expected in D1.2...
- In order to accelerate the process, Jean proposes to set up a "core team" composed of representatives of the different industrial domains (or other interested people too). Those people will work specifically on "needs" and "requirements". They will meet in specific meetings... Sebastian and Henri will participate (thanks!). A local physical meeting with people from Airbus, Thales, ADS, TAS, IRT could also be organized in order to speed up the process.  
  - [ ] (Eric) Make a call for participation to the req core team.    
  
#### New actions
- [ ] (2011-1 - Jean, Eric) Integrate Airbus' additional needs/reqs.
- [ ] (2011-2 - Eric) Make a call for participation to the req core team. 
#### Previous actions
- [ ] (0611-1 - Eric, Nicolas, Jean-Loup) Finish the discussion about "reproducibility"...
      - On going, see [this note](../documents/analysis_of_standards/2024-11-08%20-%20Replication%20criteria.md)
- [ ] (0611-2 - Eric) Prepare a followup to the discussion about computation errors: what is the impact on the MLMD?
- [X] (0611-3 - Eric) Integrate paper in [document](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md).
- [X] (0611-4 - Jean-Loup) Review the conv2d operator
      - Reviews are [here](../documents/conv_specification_example/reviews)
- [ ] (0611-5 - Eric, Mariem) Update conv2d spec from Sebastian's and Jean-Loup's reviews
  - To be done by next meeting.
- [ ] (231001 - All) Check Nicolas' classification proposal 
- [ ] (231002 - Mohammed) Propose a use case for CS, [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
      - In progress. The case study is drone tracking. Transformers are used, but the model remains "simple"  enough to be embedded...
      - To be done by next meeting.
- [X] (231002 - Jean-Baptiste) Provide a first analysis of the ARP 6983 / EASA concept paper
      - In progress. Under validation. 
      - First draft version to be delivered on next week. To be reviewed.
      - No document received as of 20/11/2024. Eric contacted Jean-Baptiste on 20/11/2024.
      - Document received on 2024/11/21, see [here](../documents/analysis_of_standards/SONNX_requirements_draft1.docx)
- [ ] (231002 - Sebastian) Get in touch with other people in the automotive partners (e.g. ETAS).
- [ ] (231002 - Luis) Provide contact(s) with other industrial domains (medical,...)
    - On-going (see previous meeting)
- [ ] (A008 - leads) Plan SC meetings
- [ ] (A009 - Dumitru) Correct  / complete description of issue #2
      - Dumitru will check this...
profile/meetings/numerical_issues/01_what_is_the_issue.md}. Please add your ideas / remarks...
      - First discussion in the 11/06 WG meeting
- [ ] (A015) All : Complete description of use cases
      - On-going
- [ ] (A016) All : Complete description of needs
      - On-going
- [ ] (A002 - all) Add / remove your name for the [participant list ](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/team.md) and provide information about your possible contribution
- [ ] (A004 - all) Propose a short communication during the next WG meetings. The list is [here](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/presentation_proposals.md).
  - [X] Sebastian Boblest (Bosch) on their tool (2024/12/18)
  - Alexandre Eichenberger (IBM),  on onnx-mlir (2025/??/??)
  - ??? on specification and verification of FP computations (2025/??/??)
  - Eduardo (Manchester U) on "Evaluation and improvement of SW verifiers on FP Neural Networks" (2025/??/??)
- [ ] (A006 - leads) Finalize the organization of the WG's repository. Define procedure to use it (inc. issues, wiki,...)
  - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18
  - Meeting moved to 2024/11/21
- [ ] (A007 - leads) Setup a mailing list
  - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18
  - Meeting moved to 2024/11/21


# 2024/11/06
## Agenda
- Review of actions
- Feedback on ``conv2d`` operator review (Sebastian)
- Computations accuracy
  - In the last meeting, we have identified that the precision (of computations) of computations are issue. This subject deserves a dedicated meeting and work. All material concerning this topics can be found [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues). A first list of questions and some "food for thought" are available [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md)
- Other events
  - [ISCLP meeting](https://www.defense.gouv.fr/dga/evenements/ouverture-inscriptions-au-seminaire-futur-lembarque-critique-systemes-combat) at DGA-TA Toulouse
  - Collab. with [DeepGreen](https://deepgreen.ai/) project about reference implementation (followup to [10/25 meeting minutes](safety-related-profile/meetings/Other_meetings/2024-10-25-DeepGreen.md) )

## Participants
JENN Eric, Adrian Evans, Pierre Gaillard, Nicolas Valot , Edoardo Manino, Jean-Loup , Julien VIDALIE, COMBES Yohann, BELCAID Mohammed, Jean-Baptiste Rouffet, Jean Souyris , Cong Liu, Jean-Loup Farges, Claire Pagetti , Thiziri Belkacem Airbus Protect , Dumitru Potop, Sebastian Boblest , Sergei CHICHIN, Boblest Sebastian, Vo Duy Khoi

## Minutes
- Discussion about computation errors (see presentation in [markdown](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/slides-06-11.md) and [pdf](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/2024-11-06%20-%20Numerical%20issues.pdf))
  - **Slide 10: About weak and strong reproducibility**\
      - Statement is not clear.\
      The idea is that complying with the specification (the MLMD) does not ensure reproducibility: if the specification allows some error with respect to the true value, an implementation may compy with the specification without complying with reproducibility. Therefore, this is another property.  How compliance with the MLMD is ensured is another problem. We may use the "reference implementation" (RI), but it only moves the problem since we will have to demonstrate compliance of the RI to the MLMD... 
      - What does "all implementation" mean?\
        It refers to the set of all *potential* implementations that would comply to the MLMD, not the *actual* set of implementations (which is a subset of the former...). 
      - About the empirical evaluation of the effects of computation errors, see paper "[Causes and effects of unanticipated numerical deviations in neural networks inference frameworks](https://proceedings.neurips.cc/paper_files/paper/2023/file/af076c3bdbf935b81d808e37c5ede463-Paper-Conference.pdf)"
      - About non-determinism: here, we only care about inference, not training ; we only consider non-determinism due to numerical computations, not other sources such as random number generators...
      - Reproducibility is also a concern for audit activities (or "auditability").
      - [ ] (Eric, Nicolas, Jean-Loup) Finish the discussion about "reproducibility"...
      - [ ] (Eric) Integrate paper in [document](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md). 
  - **Slide 12: importance of accuracy for ML**
      The effects of mathematical error may strongly depend on the type of application (e.g., regression *vs.* classification) 
  - **Slide 15: mathematical libraries**
    - There are version of ``libm`` that give explicitly accuracy requirements. See e.g., [sleef](https://github.com/shibatch/sleef/tree/master/docs/2-references/libm)
  - **Slide 17**
    - Over/under flow can be easily avoided using "accumulator" with a sufficient size. <off meeting: but overflow may occur in other situations>
    - **General** 
      - The slide are focus on the second part of the W cycle. Howver, as the MLMD is at he transition  between the two Vs, we also have to consider the relation between the ML model used during training and evaluation and the MLMD. In particular, what needs to be put in the MLMD to support the activities occuring in the ascending part of the first V (in order to ensure that the MLML delivered to the developper is correct)? 
      - In fact, what is (could be considered as) the actual reference is the model used for the training and evaluation that is executed using e.g., TensorFlow. Therefore, we shall provide all embed all the necessary information (metadata) in the MLMD to precisely designate this environment (framework, version of framework, machine, operating system,etc.). Note that the current version of ONNX aleady has this capability. <off meeting: another approach would be to consider that the evaluation of the model should be done using the reference implementation. This would really make the SONNX model THE specification.../>
  - [ ] (0611-2 - Eric) Prepare a followup to the discussion about computation errors: what is the impact on the MLMD?
  
- Review of Sebastian's remarks on the ``conv2d`` operator specification
  - Detailled remarks are in [Sebastian's branch](https://github.com/SebastianBoblest/working-groups/tree/lookAtConvSpec/safety-related-profile/documents/conv_specification_example). 
  - Major remarks:
    - Some restrictions (of the current version) prevent the description of some of the use models. For instance, the ``group`` attribute must support depthwise convolution with channel multiplier 1.
    - Many attributes of the ONNX spec are optional or "redundant" in the sense that their role can be played using other, more primitive attribnutes. For instance, the ``auto_pad`` attribute can be replaced by an explicit choice of padding. 
    - The SONNX profile shall provide a single solution without restricting capabilities ("There shall be a unique way to do things").
    - It also makes life of "customers" (aka "users") simpler.
    - The presentation is OK. The diagram must be kept, but corrected (see detailled comments)
    - [ ] (Jean-Loup) Review the conv2d operator
    - [ ] (Eric, Mariem) Update conv2d spec according to Sebastian's and Jean-Loup's reviews
  

#### New actions
- [ ] (0611-1 - Eric, Nicolas, Jean-Loup) Finish the discussion about "reproducibility"...
- [ ] (0611-2 - Eric) Prepare a followup to the discussion about computation errors: what is the impact on the MLMD?
- [ ] (0611-3 - Eric) Integrate paper in [document](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md).
- [ ] (0611-4 - Jean-Loup) Review the conv2d operator
- [ ] (0611-5 - Eric, Mariem) Update conv2d spec from Sebastian's and Jean-Loup's reviews
   
#### Previous actions
- [ ] (231001 - All) Check Nicolas' classification proposal 
- [ ] (231002 - Mohammed) Propose a use case for CS, [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
      - In progress. The case study is drone tracking. Transformers are used, but the model remains "simple"  enough to be embedded...
- [ ] (231002 - Jean-Baptiste) Provide a first analysis of the ARP 6983 / EASA concept paper
      - In progress. Under validation. 
      - First draft version to be delivered on next week. To be reviewed.
- [ ] (231002 - Sebastian) Get in touch with other people in the automotive partners (e.g. ETAS).
- [X] (231002 - Sebastian and Luis) Review of the [Conv2d operator](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example).
  - Done: to be discussed with Sebastian on 11/06
- [ ] (231002 - Luis) Provide contact(s) with other industrial domains (medical,...)
  - On-going:  
  > Regarding the invitation of experts to participate in the WG:
  > - Health sector: [METTLER]  the contacts were identified, the emails were sent, and we are waiting on their response.
  > - Railway sector: [ALSTOM] the contacts were identified.
  > Meanwhile do you think relevant to get more experts into the WG from the automotive industry (working in autonomous drive)?
  > I have good contacts in the H2020 project consortium Hi-Drive (www.hi-drive.eu [...]  Should I try to get some of them onboard?
- [X] (231002 - Eric) Provide one slide about SONNX.
  - Done: see [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/Other_meetings/2024-11%20-%20ISCLP%20meeting%20-%20SONNX.pptx)
- [ ] (A008 - leads) Plan SC meetings
  - No action.
- [ ] (A009 - Dumitru) Correct  / complete description of issue #2
      - Dumitru will check this...
- [X] (A012 - Nicolas) Review the the "issues" document
- [X] (A013 - leads) Organize a meeting on numerical computations (fp-sg)
      - Pending. Subject to be addressed durint the next meeting 2024/11/06. Draft material is available [here]{https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md}. Please add your ideas / remarks...
      - First discussion in the 11/06 WG meeting
- [ ] (A015) All : Complete description of use cases
      - Pending
- [ ] (A016) All : Complete description of needs
      - Pending
- [ ] (A002 - all) Add / remove your name for the [participant list ](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/team.md) and provide information about your possible contribution
- [ ] (A004 - all) Propose a short communication during the next WG meetings. The list is [here](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/presentation_proposals.md).
  - Sebastian Boblest (Bosch), on their tool (to be planned)
  - Alexandre Eichenberger (IBM),  on onnx-mlir (to be planned)
  - ??? on specification and verification of FP computations
- [ ] (A006 - leads) Finalize the organization of the WG's repository. Define procedure to use it (inc. issues, wiki,...)
  - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18
- [ ] (A007 - leads) Setup a mailing list
      - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18

# 2024/10/23
## Agenda
- Review of actions
- Rapid review of current contents of Use Cases and Needs
- Work sharing and commitments (who can contribute to what?)
- Work on the PoC : review of the informal description, improvements
- Other events

## Participants

JENN Eric, TURKI Mariem, Filipo PEROTTO, Julien VIDALIE, Andreas Fehlner, JB Rouffet, BELCAID Mohammed, Nicolas Valot, BELFY Henri, Luís Conde, BONNAFOUS Eric, Jean-Loup Farges, Jean Souyris, Cong Liu, Dumitru Potop, Claire Pagetti, Edoardo Manino, Sebastian Boblest  

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
  - [ ] (Luis) Provide contact(s) with medical and railway domains.
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
  - Done: to be discussed with Sebastian on 11/06
- [ ] (231002 - Luis) Provide contact(s) with other industrial domains (medical,...)

#### Previous actions
- [ ] (A008 - leads) Plan SC meetings
  - No action.
- [ ] (A009 - Dumitru) Correct  / complete description of issue #2
- [X] (A010 - leads) Create a “tools” area <closed on 03/10>
- [X] (A011 - Nicolas) Deposit his operator extraction tool in the repository. <closed on 03/10>
- [X] (A012 - Nicolas) Review the the "issues" document
- [ ] (A013 - leads) Organize a meeting on numerical computations (fp-sg)
      - Pending. Subject to be addressed durint the next meeting 2024/11/06. Draft material is available [here]{https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md}. Please add your ideas / remarks...
      - First discussion in the WG on 11/06
- [X] (A014 - fp-sg) Provide a clear statement of the numerical computations issues.
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
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18
- [ ] (A007 - leads) Setup a mailing list
      - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18

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

# SONNX meeting (04/09)

## Object
- ONNX Safety-related workgroup meeting

## Attendees
- Jean, Eric (ed.), Claire, Dumitru, Sergei, Henri, Nicolas,  Mariem
  
## Agenda
- Status of actions (see below)
  - [X]  <21/08> (Mariem) Convert the CONV operator specification to markdown. (see [here](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example))
  - [X]  <21/08> (eric+Jean) Clarifies the use of github… => SeeMariem's presentation below.
  - [X]  (eric+jean) Propose an agenda for the KOM => see text below.
  - [X]  (all) Read the SOW and provide your feedback
  - [X]  <21/08> (Eric+Jean) In the SoW, Add to the SoW activities related to the validation of the WG results through its application to a practical use case

- KOM Agenda and organisation
  - Invitation text:
  >Dear Colleague,
  > On September 25th, 17:00-19:00, we organize the kick-off meeting of the Safety-Related Profile ONNX Working Group (WG).
  > The objective of this working group is to refine and clarify the semantics and syntax of the existing ONNX standard, ensuring unequivocal interpretation of models during the implementation phase.
  > This initiative was presented to the ONNX community during the ONNX MeetUp (June 26th, 2024) and the creation of the WG was accepted by the ONNX community on July 18th, 2024.
  > You will find the slides presented during this meeting here.  We will come back to this presentation and go into more details during the KOM. 
  > The agenda is available here. 
  > The "outlook invitation" will be sent in another mail. 
  > If you want to participate and have not received this invitation directly, please send a message to Eric (eric.jenn@irt-saintexupery.com) and Jean (jean.souyris@airbus.com).
  > Looking forward to meeting you on September 25th,
  > The co-chairs,
  > Eric JENN (IRT Saint-Exupéry) et Jean SOUYRIS (Airbus)

  - Proposed agenda
      1. **Introduction**: Presentation of the general objectives of the workgroup based on the slides shown during the meetup (Eric + Jean, 10 min)
      2. **Phase 1: Why?**
         1. Presentation of an example of regulatory requirements: the ARP. (Christophe, 15 min)
         2. Presentation of a few examples of issues posed by the current standard, choosing problems of various natures (Nicolas, 15 min)
      3. **Phase 2: What?**
         1. Presentation of an example of a set of requirements (???, to be prepared, 10 min)
         2. Presentation of an example of what the output of the work could be for the specification of an operator (Mariem + Eric, 15 min)
      4. **Phase 3: How?**
         1. Presentation of the work plan and the organization of the working group (Eric + Jean, 15 min)
         2. Brief presentation of the "hard points" that we have already identified (10 min)
      5. **Discussion** (All, 30 min)
      - Use of Github: See _Mariem presentation_
    
- Workplan (simplified)
    - See [here](https://extranet.irt-saintexupery.com/Extranet/Projets/SONNX/Work/_layouts/15/WopiFrame.aspx?sourcedoc=/Extranet/Projets/SONNX/Work/Documents%20partages/Admin/Workplan.xlsx&action=default)

## Minutes
- Discussion about the github structure and management.
    - Question was raised about the nature of the document we could put on the github:
      - The principle is that ANY document put on our repo is publicly accessible. So, **no document with restiction** shall be placed in the repo.
      - Concerning the possible publications of the workgroup, we will use a private Overleaf (e.g.) account to work in common. 
    - Mariem has reminded us the (usual) way to use github. See her [slides](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/procedures/ModifGithubONNX.pdf)
    - This approach seems a bit complicated, especially if we are working in common on documents.It is necessary because the project is public and so requires some control before accepting modifications. Using a private project could be simpler. 
    - [X] (05/09) Henri to propose document edition / sharing modalities
      - See [proposal](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/procedures/collaborative_docs.md)
    - Currently, we are working on Eric's branch that is hosted in a private account (github.com/ericjenn/...). It may be cleaner to use a specific account for our workgroup (e.g., github.com/sonnx./...)

## Actions
  - [ ] (09/09) Eric to check if we could create a SONNX account in github
  - [ ] (05/09) Eric to check with Ram if there is any "rule"/ "contraint" imposed by ONNX on the use of github 
  - [X] (05/09) Henri to propose document edition / sharing modalities
    - See [proposal]()
  - [ ]  <21/08> (Mariem, eric, Loïc) Propose an first axiomatization of tensors (3D, 4D) and use it to specify the CONV operator.
  - [ ]  <21/08> (Mariem, Loïc, Eric, Augustin) Specify the CONV operator for int8 and (e.g., ) float16….
  - [ ]  <21/08> (Eric+Jean) In the SoW, avoid the use of the term “ambiguity”. Be more explicit about the different types of requirements. Introduce the concept of "replication" 
  - [ ]  <10/07>(eric+jean) Organize some meetings as “advisory boards”

# SONNX meeting (21/08)

## Object

- ONNX Safety-related workgroup meeting

## Attendees

- Mariem, Nicolas, Augustin, Eric

## Minutes

- Status of actions (see below)
- Brief recap of the work done on the CONV operator (Mariem)
    - The Why3 specification is now complete thanks to Loïc. A FrameC implementation is also available.
        
        
        - [ ]  <21/08> (Mariem) Convert the CONV operator specification to markdown.
    - After discussion with Loïc, the appropriate solution would be first to “axiomatize” tensors (in the same way it has already been done for matrices).
        
        
        - [ ]  <21/08> (Mariem, eric, Loïc) Propose an first axiomatization of tensors (3D, 4D) and use it to specify the CONV operator.
- Discussion of Nicolas’ comments on the SOW
    - Four points were discussed
        - We have introduced new terms (”TMD, TMDL) that are neither used in the ONNX community (where the term “ONNX IR” is used) nor in the ARP (where the term “MLMD” is used). We have either to stick to one of those — possibly ONNX’ — or at least explain the correspondence between them…
        - Nicolas mentioned that we have to “address the semantic of the model storage (ONNX IR for safety critical) […]”.
            - Yes, this should be covered by the activities concerning the semantics and the syntax of the model description language. Nicolas also raised the question about discriminating the model used during the design and the model used as the starting point of the implementation. *But it is not clear whether we really need to discriminate them: we are only concerned by the semantics of the model, whatever its used.* However, we will not consider operators used during training, so our profile will only be applicable during inference…
        - Nicolas what not happy with the remark about “ambiguous” models  (sentence  “[…] ambiguous if this ambiguity is acceptable or even necessary to leave some freedom to the implementer […]): *I do not see any reason for that. The model shall be unambiguous. If the implementer chooses to implement a surrogate model (optimized), then this model is the MLMD to be specified using ONNX. ARP6983 specifies that replication criteria shall be specified*.
            - This is an important point. The model shall actually be non ambiguous. The user may introduce derived requirements about implementation (e.g., the order in which operators have to be executed). This contingency is what was meant by the term “ambiguity”. We have to be more explicit in the SoW: the specification will not be ambiguous, but there will be some “flexibility” about the set of derived requirements applicable to a given model.
            
            - [ ]  <21/08> (Eric+Jeans) In the SoW, avoid the use of the term “ambiguity”. Be more explicit about the different types of requirements. Introduce the concept of “replication criteria” and clarify its relation to requirements.
        - Nicolas mentioned that “All the activities consist in paper work. Is there some room for POC for formal verification, extension of the definition of the format, tools to build, review, verify a SONNX MLMD ? Who are the users/recipients of the outputs ? (I would guess that some output are for us, some others for ONNX community...).”
            - Only the first part of the remark was discussed: we actually need some “practical” work in order to validate our proposal. We should introduce a “running example” (e.g., MobileNet) that will be specified using SONNX, implemented, compared with a reference implementation, etc.  Those “practical” implementation activities have to be described in the SoW too.
                
                
                - [ ]  <21/08> (Eric+Jeans) Add to the SoW activities related to the validation of the WG results through its application to a practical use case
- Discussion about polymorphic operators: *we have to provide a specific specification for every types supported by an operator,* i.e., there will be a specification of the CONV operator for int8, float16, etc. This is in particular necessary for ints for which saturation is necessary. We should do the exercise on the CONV operator.
    
    
    - [ ]  <21/08> (Mariem, Loïc, Eric, Augustin) Specify the CONV operator for int8 and (e.g., ) float16….
- We have to specify the broadcasting rules (see [https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md](https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md)).
- Logistics
    - All documents should be in the same place. At the moment, some documents are on the IRT’s sharepoint while some other at in the ONNX github. Office documents where placed in the Sharepoint for they were directly editable by some users. For other (e.g., Airbus), Sharepoint documents need to be downloaded first, which make Sharepoint pointless. 
    - [X]  <21/08> (Eric) Convert the SOW to markdown, move all documents to github
        - Documents have moved [here](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents).
    - The Sharepoint has moved in order to match the new project name, which is “SONNX”. The URL is now : [https://extranet.irt-saintexupery.com/Extranet/Projets/SONNX/Pages/default.aspx](https://extranet.irt-saintexupery.com/Extranet/Projets/SONNX/Pages/default.aspx)
    - The github repository is accessible at  [https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile).
    
    - [ ]  <21/08> (eric+Jean) Clarifies the use of github…
    

## Actions

- [x]  (eric) Put the examples of mails (in French and English) to be used for dissemination purposes.

- [x]  (eric) Propose a poll for the project’s name, (all) answer the poll
    - (Updated 21/08) SONNX

- [ ]  (eric+jean) Propose an agenda for the KOM

- [ ]  (all) Read the SOW and provide your feedback )
- (Updated 21/08) Comments by Nicolas, see doc.

- [x]  (Nicolas) Collect the analysis done so far and put it in one document (on sharepoint or on the ONNX git, it’s up to you)
    - Done, the document is on the sharepoint ([https://extranet.irt-saintexupery.com/Extranet/Projets/SONNX/Work/_layouts/15/WopiFrame.aspx?sourcedoc=/Extranet/Projets/SONNX/Work/Documents partages/SoW/ONNX format comments v0.1.docx&action=default](https://extranet.irt-saintexupery.com/Extranet/Projets/SONNX/Work/_layouts/15/WopiFrame.aspx?sourcedoc=/Extranet/Projets/SONNX/Work/Documents%20partages/SoW/ONNX%20format%20comments%20v0.1.docx&action=default)”)

- [ ]  <10/07>(eric+jean) Organize some meetings as “advisory boards”
- [x]  <21/08> (Eric) Convert the SOW to markdown
