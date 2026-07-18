### **Participants**  
- **Franck VEDRINE** (CEA, developer of the Fluctuat tool)  
- **Mariem TURKI** (IRT St-Ex)  
- **Jean SOUYRIS** (Airbus)  
- **Eric JENN** (IRT St-Ex)  

### **Subject:**  
- Introduction of the SONNX working group to Franck  
- Open discussion and potential directions  

### **Discussion Summary**  

- **Initial Focus:**  
  - We will first concentrate on networks using:  
    - **Integer data (quantized networks)**, e.g., int8.  
    - **Floating-point data** (16, 32, and 64-bit), provided they comply with the IEEE standard.  

- **Analogy with SCADE Operators:**  
  - There are parallels between our work on graph operators and SCADE operators. The requirements are quite similar, but differences lie in:  
    - The sheer volume of operations (much higher in neural networks).  
    - The challenge of assessing the impact of computational errors on function performance (e.g., how does an error in an operator affect the final decision?).  
  - In any case, it seems difficult to specify error objectives (relative or absolute)* at the operator level.  
    - Even in more conventional cases, such requirements are rarely defined *a priori*, except in specific scenarios.  

- **Current Approach:**  
  - More "pragmatic"—determining the maximum error that can be guaranteed with a given effort (*best effort*).  
  - This error becomes the *de facto* specification, as it can be accounted for at the system level (e.g., for filtering functions).  

- **Error Evaluation Considerations:**  
  - Must account for:  
    - **Method-related errors**  
    - **Implementation-related errors**  
  - Currently, SONNX does **not** specify the method or implementation, so this approach is not directly applicable at this level.  

- **Reference Implementation Level:**  
  - An **error estimate** can be provided for the reference implementation.  
  - **Caution:**  
    - This error might only be achievable in a simple implementation and degrade in more complex, optimized versions.  
    - This could lead to specifying unrealistic error bounds.  
  - **Proposal:** Provide estimates for multiple implementations:  
    - A simple one (our "reference implementation" via Why3), easier to analyze but potentially less efficient.  
    - A more complex, optimized one.  
  - **Key Points:**  
    - In critical domains, implementations should remain relatively simple.  
    - Otherwise, applicants are free to develop their own implementation and apply the recommended method.  

- **Error Evaluation Categories:**  
  To handle a wide range of cases (including complex ones without formal estimates), evaluations could be categorized as:  
  - **Bronze:** Incomplete error assessment.  
  - **Silver:** Abstract interpretation (Fluctuat).  
  - **Gold:** Axiomatic proof.  

- **Alternative Approach:**  
  - We could also simply describe the error estimation method.  
  - However, whenever possible, we will aim to provide tools for estimating the error, potentially as:  
    - An **analytical expression**.  
    - A **calculation program** (if the error depends on input tensor characteristics, e.g., dimensions and size).  

- **Input Domain Constraints:**  
  - In some use cases, input parameter ranges may be bounded and known (e.g., values in [-1, 1]).  
    - Such constraints could improve error estimation accuracy.  
    - Further study is needed to determine when these apply.  

- **Benefits of Error Estimation:**  
  - Facilitates model debugging by identifying error sources.  
  - Enables post-mortem analysis/diagnostics in case of failure.  
  - Provides insights into the origin of output errors.  

- **Next Steps with Franck:**  
  - Franck expressed interest in the topic and agreed to join the working group.  
  - **Actions:**  
    - [X] Send meeting invitations.  
    - [X] Share document links.  
    - [X] Grant Git access.  


