let
    Source = MySQL.Database("localhost:3306", "customer_behavior", [ReturnSingleDatabase=true]),
    customer = Source{[Schema="customer_behavior",Item="customer"]}[Data]
in
    customer
