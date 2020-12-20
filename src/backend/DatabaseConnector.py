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

    def get_birds_area(self, kind=None):
        with self.driver.session() as session:
            area = session.write_transaction(self._get_birds_area, kind)
        return area

    def get_all_birds_area(self):
        with self.driver.session() as session:
            area = session.write_transaction(self._get_all_birds_area)
            print(area)
        return area

    def create_bird(self, url, name, latitude, longitude):
        with self.driver.session() as session:
            birdId = self.countBirds()
            bird = session.write_transaction(self._create_bird, birdId, url, name, latitude, longitude)

    def delete_nodes(self):
        with self.driver.session() as session:
            session.write_transaction(self._delete_nodes)

    # def delete_nodes(self):
    #     with self.driver.session() as session:
    #         session.write_transaction(self._delete_nodes)

    def getSpecies(self):
        with self.driver.session() as session:
            result = session.write_transaction(self._get_all_species)
            return result

    def createSpec(self, name):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_species, name)

    # That returns greeting message
    def getCsv(self):
        with self.driver.session() as session:
            result = session.write_transaction(self._get_data)[0]
        return result

    def setCsv(self):
        with self.driver.session() as session:
            session.write_transaction(self._import)

    def countBirds(self):
        with self.driver.session() as session:
            result = session.write_transaction(self._count_birds)
        return result["count"]

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

    # Get id's of all birds by its kind
    @staticmethod
    def _select_by_kind(tx, kind):
        req = '''MATCH (id:Bird)-[:is]->(Kind {name: $kind})
                 RETURN id'''
        result = tx.run(req, kind=kind)
        return [record["id"] for record in result]

    # Get the bird by id
    @staticmethod
    def _select_by_id(tx, id_):
        req = '''MATCH (a:Bird {Bird_id: $id_})
                 RETURN a'''
        result = tx.run(req, id_=id_)
        return result.single()

    # Get all of these flying creatures
    @staticmethod
    def _select_all(tx):
        req = '''MATCH (a:Bird)
                 RETURN a'''
        result = tx.run(req)
        return result

    # Show the birds flying area by its kind
    @staticmethod
    def _get_birds_area(tx, kind=None):
        req = '''MATCH (a:Bird)-[:Found_at]->(b:Place)
                 MATCH (:Bird)-[:Is]->(c:Kind)
                 WHERE (a)-[:Is]->(c) AND c.name = $kind
                 RETURN b'''
        result = tx.run(req, kind=kind)
        return [{'latitude':place[0]['latitude'], 'longitude':place[0]['longitude']} for place in result.values()] # [rec['latitude'] for rec in result]

    @staticmethod
    def _get_all_birds_area(tx):
        req = '''MATCH (a:Bird)-[:Found_at]->(b:Place)
                 RETURN b'''
        result = tx.run(req)
        return [{'latitude':place[0]['latitude'], 'longitude':place[0]['longitude']}for place in
                result.values()]  # [rec['latitude'] for rec in result]

    @staticmethod
    def _create_bird(tx, id__, url, name, latitude, longitude):
        req = '''CREATE (a:Bird {Bird_id: $id__})
                 CREATE (c:Kind {name: $name})
                 CREATE (b:File {URL: $url})
                 CREATE (d:Place {latitude: $latitude, longitude: $longitude})
                 CREATE (a)-[:Is]->(c)
                 CREATE (a)-[:Contains]->(b)
                 CREATE (a)-[:Found_at]->(d)
        '''
        return tx.run(req, id__=id__, url=url, name=name, latitude=latitude, longitude=longitude)

    @staticmethod
    def _count_birds(tx):
        req = '''MATCH (n:Bird) RETURN COUNT(n) as count'''
        result = tx.run(req)  # A dictionary or something
        return result.single()

    @staticmethod
    def _delete_nodes(tx):
        req = '''MATCH (n) DETACH DELETE n'''
        result = tx.run(req)
        return result

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
    # print(greeter.getSpecies())
    # greeter.delete_nodes()
    # print(greeter.create_bird(0, 1, "Грач", 0.1, 0.2))
    # print(greeter.create_bird(1, 1, "Птеродактиль", 0.3, 0.4))
    # print(greeter.create_bird(2, 1, "Соловей", 0.5, 0.6))
    # print(greeter.create_bird(3, 1, "Грач", 0.7, 0.8))
    # print(greeter.get_birds_area("Грач"))

    print(greeter.countBirds())
    greeter.close()


    # rec = greeter.getCsv()
    # print(rec)
    # print(type(rec))
    # greeter.createSpec('extra spec')
    # greeter.setCsv()
    # greeter.close()
    #

