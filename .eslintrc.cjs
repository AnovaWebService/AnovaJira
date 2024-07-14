const configs = [
  {
    files: ['.eslintrc.js'],
    env: {node: true},
  },
  {
    files: ['vite.config.ts'],
    rules: {
      'import/prefer-default-export': ['error', {target: 'single'}],
      'no-restricted-exports': 'off',
    },
  },
];

module.exports = {
  root: true,
  extends: [
    'plugin:security/recommended-legacy',
    'plugin:react-hooks/recommended',
    'plugin:prettier/recommended',
  ],
  parser: '@typescript-eslint/parser',
  plugins: [
    '@stylistic/ts',
    'import',
    'react',
    'unicorn',
    '@typescript-eslint',
    'perfectionist',
    'unused-imports',
  ],
  settings: {
    react: {
      version: 'detect',
    },
  },
  overrides: [
    {
      files: ['*.ts?(x)'],
      parserOptions: {
        tsconfigRootDir: __dirname,
        project: './tsconfig.json',
      },
      rules: {
        '@typescript-eslint/await-thenable': 'error',
      },
    },
    ...configs,
  ],
  rules: {
    // ! ERRORS

    'no-restricted-exports': [
      'error',
      {
        restrictDefaultExports: {
          direct: true,
          named: true,
          defaultFrom: true,
          namedFrom: true,
          namespaceFrom: true,
        },
      },
    ],

    'unicorn/filename-case': ['error', {case: 'kebabCase'}],

    'react/function-component-definition': [
      'error',
      {ops: {namedComponents: 'function-declaration'}},
    ],
    'react/jsx-handler-names': [
      'error',
      {
        eventHandlerPrefix: 'handle',
        eventHandlerPropPrefix: 'on',
        checkLocalVariables: true,
        checkInlineFunction: false,
      },
    ],
    'react/no-children-prop': 'error',
    'react/jsx-pascal-case': [
      'error',
      {allowAllCaps: true, allowNamespace: true, allowLeadingUnderscore: true},
    ],
    'react/display-name': 'error',
    'react/jsx-filename-extension': ['error', {extensions: ['.tsx', '.jsx']}],
    'react/jsx-key': ['error', {checkFragmentShorthand: true}],
    'react/no-object-type-as-default-prop': 'error',
    'react/no-array-index-key': 'error',
    'react/no-danger-with-children': 'error',
    'react/no-this-in-sfc': 'error',
    'react/style-prop-object': 'error',
    'react/void-dom-elements-no-children': 'error',

    'import/no-mutable-exports': 'error',
    'import/named': 'error',
    'import/namespace': 'error',
    'import/default': 'error',
    'import/export': 'error',
    'import/no-named-as-default': 'error',
    'import/no-named-as-default-member': 'error',

    // * WARNINGS

    'no-console': 'warn',

    'perfectionist/sort-named-imports': 'warn',
    'perfectionist/sort-imports': ['warn',{
      groups: [
        ['builtin', 'external'],
        ['type','internal-type','parent-type', 'sibling-type', 'index-type'],
        ['internal', 'parent', 'sibling', 'index'],
        'object',
        'unknown',
      ]
    }],

    'prettier/prettier': 'warn',

    'unused-imports/no-unused-imports': 'warn',
    'unused-imports/no-unused-vars': [
      'warn',
      {
        vars: 'all',
        args: 'after-used',
      },
    ],

    'import/no-duplicates': 'warn',
    'import/consistent-type-specifier-style': 'warn',

    '@stylistic/ts/function-call-spacing': ['warn', 'never'],
    '@stylistic/ts/lines-between-class-members': 'warn',

    '@typescript-eslint/array-type': [
      'warn',
      {default: 'array-simple', readonly: 'array-simple'},
    ],
    '@typescript-eslint/ban-types': 'warn',

    'react/destructuring-assignment': [
      'warn',
      'always',
      {destructureInSignature: 'always'},
    ],
    'react/jsx-boolean-value': ['warn', 'never'],
    'react/jsx-curly-brace-presence': [
      'warn',
      {props: 'never', children: 'never', propElementValues: 'always'},
    ],
    'react/jsx-fragments': ['warn', 'syntax'],
    'react/jsx-no-leaked-render': 'warn',
    'react/jsx-no-useless-fragment': 'warn',
    'react/prefer-read-only-props': 'warn',
    'react/self-closing-comp': 'warn',

    // ? DISABLED

    'react-hooks/exhaustive-deps': 'off',
  },
};
