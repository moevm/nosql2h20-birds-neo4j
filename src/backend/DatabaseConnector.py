from neo4j import GraphDatabase


class DatabaseConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    def getSpecies(self):
        with self.driver.session() as session:
            result = session.write_transaction(self._get_all_species)
            return result

    def createSpec(self, name):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_species, name)

    # That returns greeting message
    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    # That returns a list of all the species represented
    @staticmethod
    def _get_all_species(tx):
        req = '''MATCH (n:Kind)
                 RETURN n.name as name'''
        result = tx.run(req)  # A dictionary or something
        return [record["name"] for record in result]  # Make namelist of it

    # Create bird's kind
    @staticmethod
    def _create_species(tx, name):
        req = '''MATCH (a:Kind)
                 SET a.name = $name '''
        result = tx.run(req, name=name)
        return result.single()

    # Select all birds by kind
    @staticmethod
    def _select_by_kind(tx, kind):
        req = '''MATCH (id:Bird)-[:is]->(Kind {name: $kind})
                 RETURN id'''
        result = tx.run(req)
        return [record["id"] for record in result]







if __name__ == "__main__":
    greeter = DatabaseConnector("bolt://localhost:7687", "neo4j", "password")
    # greeter.print_greeting("hello, world")
    print(greeter.getSpecies())
    greeter.close()
