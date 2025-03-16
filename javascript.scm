(
  [(function_declaration) (generator_function_declaration)] @function
)

(
    (arrow_function
    parameters: (formal_parameters) @function.parameters
    body: (expression) @function.body
    ) @function
)

(
  (lexical_declaration
    (variable_declarator
      name: (identifier) @name
      value: [(arrow_function) (function_expression)]) @function)
)

(
  (variable_declaration
    (variable_declarator
      name: (identifier) @name
      value: [(arrow_function) (function_expression)]) @function)
)

(
  (lexical_declaration
    (variable_declarator
      name: (identifier) @object.name
      value: (object
        (pair
          key: (property_identifier) @name
          value: [(arrow_function) (function_expression) (generator_function) (method_definition)] @function
        )
      )
    )
  )
)

(
  (variable_declaration
    (variable_declarator
      name: (identifier) @object.name
      value: (object
        (pair
          key: (property_identifier) @name
          value: [(arrow_function) (function_expression) (generator_function) (method_definition)]
        ) @function
      ) 
    )
  )
)