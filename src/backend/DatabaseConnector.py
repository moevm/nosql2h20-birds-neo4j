from neo4j import GraphDatabase
from neomodel import db, clear_neo4j_database


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

    def getCsv(self):
        with self.driver.session() as session:
            result = session.write_transaction(self._get_data)[0]
        return result

    def setCsv(self):
        with self.driver.session() as session:
            session.write_transaction(self._import)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    # That returns a list of all the species represented
    @staticmethod
    def _get_all_species(tx):
        req = '''MATCH (n:Species)
                 RETURN n.name as name'''
        result = tx.run(req)  # A dictionary or something
        return [record["name"] for record in result]  # Make namelist of it

    @staticmethod
    def _create_species(tx, name):
        req = '''CREATE (a:Species)
                 SET a.name = $name '''
        result = tx.run(req, name=name)
        return result.single()

    @staticmethod
    def _get_data(tx):
        req = '''
            CALL apoc.export.csv.all(null, {stream: true})
            YIELD data
            RETURN data;
        '''
        result = tx.run(req)
        return result.single()

    @staticmethod
    def _import(tx):
        # That is a proto. In real life it must be as much requests and files as there are node types
        # TODO: make requests for every node type
        # TODO: format the request string with export file name
        req = '''
            load csv with headers from 'file:///file.csv' as row
                        create (:Air_class{
                                id: toInteger(row._id),
                                _labels:row._labels,
                                message:row.message
                            }
                        )
        '''
        tx.run('MATCH (n) DELETE n')  # clear database
        tx.run(req)


if __name__ == "__main__":
    greeter = DatabaseConnector("bolt://localhost:7687", "neo4j", "password")
    # greeter.print_greeting("hello, world")
    # rec = greeter.getCsv()
    # print(rec)
    # print(type(rec))
    # greeter.createSpec('extra spec')
    greeter.setCsv()
    greeter.close()
    #
