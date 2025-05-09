describe('Todo item functionality', () => {
  // Define variables that we need on multiple occasions
  let task_id
  let user_id
  let email
  let task_title

  before(function () {

    // Create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          user_id = response.body._id.$oid
          email = user.email
        })
      })

    // Create a fabricated task from a fixture
    cy.fixture('task.json')
      .then((task) => {
        task['userid'] = user_id
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/tasks/create',
          form: true,
          body: task
        }).then((response) => {
          task_id = response.body[0]._id.$oid
          task_title = task.title
        })
      })

  })

  beforeEach(function() {

    // Delete old todos
    cy.request({
      method: 'GET',
      url: `http://localhost:5000/tasks/byid/${task_id}`
    }).then((response) => {
      const todos = response.body.todos
      todos.forEach(todo => {
        cy.request({
          method: 'DELETE',
          url: `http://localhost:5000/todos/byid/${todo._id.$oid}`
        }).then((response) => {
          cy.log(response)
        })
      })
    })
  
    // Create a uncompleted todo 
    cy.fixture('todo_uncompleted.json')
      .then((todo) => {
        todo['taskid'] = task_id
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/todos/create',
          form: true,
          body: todo
        }).then((response) => {
          cy.log(response)
        })
      })

    // Create a completed todo
    cy.fixture('todo_completed.json')
      .then((todo) => {
        todo['taskid'] = task_id
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/todos/create',
          form: true,
          body: todo
        }).then((response) => {
          cy.log(response)
        })
      })
    
    // Increase size of viewport to assure that all UI elemetns are within view
    cy.viewport(1200, 1000)

    // Enter the main main page
    cy.visit('http://localhost:3000')

    // Detect a div which contains "Email Address", find the input and type
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    // Submit the form on this page
    cy.get('form')
      .submit()

    // Open task
    cy.contains('div', task_title)
      .click()
    
  })


  it('Can add todo with description', () => {
    const todo_text = 'test text for todo'

    cy.get('.inline-form > [type="text"]')
      .type(todo_text)

    cy.get('.inline-form > [type="submit"]')
      .click()
    
    cy.contains('div', todo_text)
      .should('contain.text', todo_text)

  })

  it('Can not add todo with no description', () => {

    cy.get('.inline-form > [type="submit"]')
      .should('be.disabled')

  })

  it('Mark todo to done', () => {
  
    cy.get(':nth-child(1) > .checker')
      .click()
      .should('have.class', 'checked')

    cy.get('.todo-list > :nth-child(1) > .editable')
      .should('have.css', 'text-decoration')
      .and('contain', 'line-through');
  })

  it('Unmark todo to undone', () => {

    cy.get(':nth-child(2) > .checker')
      .click()
      .should('have.class', 'unchecked')

    cy.get('.todo-list > :nth-child(2) > .editable')
      .should('have.css', 'text-decoration')
      .and('not.contain', 'line-through');

  })

  it('Remove todo item', () => {

    cy.get(':nth-child(2) > .remover')
      .click()
      
    cy.get('.todo-list > :nth-child(2)')
      .should('not.exist')

  })


  after(function () {
    // Clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${user_id}`
    }).then((response) => {
      cy.log(response.body)
    })
  })


})