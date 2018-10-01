# AI_log
This repo is having python,shell and yaml file to anaylze out.log


Brief description :
> The log_processing.py would load YAML file of rules defined and execute each function with specific
  rule variable in YAML file
> eiditing the YAML file would load different rules

Assumption :
> log file format remains same

complexity:
> analyzing new rules defined in YAML and comeup with generic function which automatically executes the 
  rules on a file
> analyzing log file for additional formats and evaluate the same

few improvements :
a. graphical representation of outputs like error / success count between a timestamp
b. added try catch block with relevant exceptions for each functions ,like
  - file not found
  - invalid inputs
c. would have implemented polymorphism , especially for historgram_error and check_number_error
d. written as seperate python modules for each use case
e. histogram_error function could have improved to show errors within specific time as well


  
