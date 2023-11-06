# *Messages Log*

MessagesLog is a module that keeps the data of all CRUD movements made in the Article (including Category and Value), Customer and Order modules.

To accomplish this goal we make use of django signals ([link](https://docs.djangoproject.com/en/4.2/topics/signals/#connecting-to-signals-sent-by-specific-senders)).

The use of signals in django in this case can be very similar to the Mediator ([link](https://refactoring.guru/es/design-patterns/mediator/python/example#example-0)). pattern, where the signals take the role of Mediator, sending the signal to MessagesLog that another model (articles, orders, etc) has changed state and must perform an action. In particular, an object of type MessagesLog will be created.

``` mermaid
sequenceDiagram
    box rgb(255, 182, 174) articles
    participant Article
    participant Category
    participant Value
    end
    box rgb(255, 225, 174) orders
    participant Order
    end
    box rgb(250, 252, 175) customers
    participant Customer
    end
    participant signals
    box rgb(176, 242, 194) messageslog
    participant MessageLog
    end

    Article->>signals: Create/Update/Delete
    activate signals
    Category->>signals: Create/Update/Delete
    activate signals
    Value->>signals: Create/Update/Delete
    activate signals
    Order->>signals: Create/Update/Delete
    activate signals
    Customer->>signals: Create/Update/Delete
    activate signals
    signals->>MessageLog: Create MessageLog object
    activate MessageLog
    deactivate signals

```

## Unit Tests

To run the unit tests of the following module please follow the instructions below

```python
asd asd py
```