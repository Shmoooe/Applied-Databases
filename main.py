from connect_mysql import connect_mysql
import datetime
from connect_neo4j import connect_neo4j

conn= connect_mysql()
connect_neo4j()

def view_directors():
    name = input("Enter director name: ")
    
    if(not conn):
        connect()
        
    query = """
            SELECT d.DirectorName, f.FilmName, s.StudioName
            FROM director d
            INNER JOIN film f ON f.FilmDirectorID = d.DirectorID
            INNER JOIN studio s ON s.StudioID = f.FilmStudioID
            WHERE d.DirectorName LIKE %s
            """
            
    cursor = conn.cursor()
    cursor.execute(query, ("%" + name + "%",))
    results = cursor.fetchall()
    cursor.close
        
    if results:
        print(f"\nFilm details for: {name}\n----------------------------\n")
        for row in results:
            print(f"{row['DirectorName']} | {row['FilmName']} | {row['StudioName']}")
    else:
        print(f"No directors of that name found\n")
            
def month_of_birth():
    while True:
        month = input("Enter month: ")
        if month.isdigit():
            month_num = int(month)
            if month_num <= 1 or month_num <= 12:
                query = """
                        SELECT ActorName, DATE(ActorDOB), ActorGender
                        FROM actor
                        WHERE MONTH(ActorDOB) = %s;
                        """
                break
            else:
                continue
            
        elif len(month) <= 3:
            query = """
                    SELECT ActorName, DATE(ActorDOB), ActorGender
                    FROM actor
                    WHERE LEFT(MONTHNAME(ActorDOB), 3) = %s
                    """
            break
        else:
            continue
            
    if(not conn):
        connect()
        
    cursor = conn.cursor()
    cursor.execute(query, (month,))
    results = cursor.fetchall()
    cursor.close()
    
    if results:
        print(f"\nActors born in month {month}:\n------------------------")
        for row in results:
            print(f"{row['ActorName']} | {row['DATE(ActorDOB)']} | {row['ActorGender']}")
            
    else:
        print("No actors found born in that month.")
        
def add_new_actor():
    print("\nAdd New Actor\n------------------------")
    
    while True:
        try:
            actor_id = int(input("Actor ID: "))
        except ValueError:
            print("Actor ID must be a number.")
            continue
  
        
        if(not conn):
            connect()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM actor WHERE ActorID = %s", (actor_id,))
                existing = cursor.fetchone()
                if existing:
                    print(f"*** ERROR *** Actor ID: {actor_id} already exists. Please choose a different ID.")
                    continue
                else:
                    break
                    
        except Exception as e:
            print(f"Database error while checking ID: {e}")
            return
    
    while True:
        actor_name = input("Actor name: ").strip()
        if actor_name:
            break
        print("Actor name cannot be empty.")
        
    while True:
        actor_dob = input("DOB: ").strip()
        try:
            parsed_date = datetime.datetime.strptime(actor_dob, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    
    while True:    
        actor_gender = input("Gender: ").strip()
        if actor_gender not in ("Male", "Female"):
            print("Gender must be 'Male' or 'Female'")
            continue
        else:
            break
            
    while True:
        try:
            actor_country_id = int(input("Country ID: "))
        except ValueError:
            print("Country ID must be a number.")
            continue
                   
        if(not conn):
            connect()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM country WHERE CountryID = %s", (actor_country_id,))
                existing = cursor.fetchone()
                if existing:
                    break
                else:
                    print(f"*** ERROR *** Country ID: {actor_country_id} does not exist.")
        
        except Exception as e:
            print(f"Database error while checking ID: {e}")
            return
 
    query = """
            INSERT INTO actor (ActorID, ActorName, ActorDOB, ActorGender, ActorCountryID)
            VALUES (%s, %s, %s, %s, %s)
            """
        
    cursor = conn.cursor()
    cursor.execute(query, (actor_id, actor_name, actor_dob, actor_gender, actor_country_id,))
    conn.commit()  
    print("Actor successfully added!")
    
driver = connect_neo4j()
    
def view_married_actors():
    try:
        actor_id = int(input("Enter ActorID: "))
    except ValueError:
            print("Actor ID must be a number.")
            return 
    
    with driver.session() as session:
        neo_query = """
        MATCH(a:Actor{ActorID:$ActorID})-[r:MARRIED_TO]->(a1:Actor) return a.ActorID, a1.ActorID
        """
        results = session.run(neo_query, ActorID=actor_id)
        married_ids=[(record["a.ActorID"], record["a1.ActorID"]) for record in results]
    
        
    if not married_ids:
        print("This actor is not married.")
        return 
        
    try:
        with conn.cursor() as cursor:
            actor_ids = [actor for pair in married_ids for actor in pair]
            placeholders= ','.join(['%s'] * len(actor_ids))
            mysql_query= f"""
            SELECT ActorID, ActorName FROM actor WHERE ActorID IN ({placeholders})
            """
            cursor.execute(mysql_query, actor_ids)
            results = cursor.fetchall()
            
            print("\n---------------\nThese actors are married:\n")
            for row in results:
                print(f"{row['ActorID']} | {row['ActorName']}")
    except Exception as e:
        print(f"MySQL error: {e}")
    
def add_actor_marriage():
    try:
        actor1_id= int(input("Enter actor 1 ID: "))
        actor2_id= int(input("Enter actor 2 ID: "))
    except ValueError:
        print("Actor IDs must be numbers.")
        return
        
    if actor1_id == actor2_id:
        print("An actor cannot marry him/herself.")
        
    try:
        with conn.cursor() as cursor:
            mysql_query = """
            SELECT  ActorID FROM actor WHERE ActorID IN (%s, %s)
            """
            cursor.execute(mysql_query, (actor1_id, actor2_id))
            results = cursor.fetchall()
            if len(results) < 2:
                print("One or both ActorIDS do not exist in the MySQL database.")
                return
                       
    except Exception as e:
        print(f"MySQL error: {e}")
        return
        
    with driver.session() as session:
        neo_check_query = """
        MATCH(a:Actor)-[:MARRIED_TO]-()
        WHERE a.ActorID IN [$id1, $id2]
        RETURN a.ActorID AS MarriedID
        """
        result = session.run(neo_check_query, id1=actor1_id, id2=actor2_id)
        married_ids = [record["MarriedID"] for record in result]
        
        actor1_married = actor1_id in married_ids
        actor2_married = actor2_id in married_ids
        
        if actor1_married and actor2_married:
            print(f"Cannot marry. Both actors are already married.")
            return
            
        elif actor1_married:
            print(f"Cannot marry. Actor {actor1_id} is already married.")
            return
            
        elif actor2_married:
            print(f"Cannot marry. Actor {actor2_id} is already married.")
            return
            
        neo_create_query = """
        MATCH(a1:Actor {ActorID: $id1}, (a2:Actor {ActorID: $id2}
        MERGE (a1)-[:MARRIED_TO]->(a2)
        """
        session.run(neo_create_query, id1=actor1_id, id2=actor2_id)
        print(f"Actor{actor1_id} is now married to actor {actor2_id}.")
        
def view_studios():
    query = """
    SELECT * FROM studio
    ORDER BY StudioID;
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query,)
            results = cursor.fetchall()
            for row in results:
                print(f"{row['StudioID']} | {row['StudioName']}")
                    
    except Exception as e:
        print(f"Database error: {e}")
        return
        
def menu():
    while True:
        print("MoviesDB")
        print("---------")
        print("\n\nMENU\n====")
        print("1 - View Directors & Films")
        print("2 - View Actors by Month of Birth")
        print("3 - Add New Actor")
        print("4 - View Married Actors")
        print("5 - Add Actor Marriage")
        print("6 - View Studios")
        print("x - Exit Application")
        choice = input("Choice: ")
        
        if choice == "1":
            view_directors()
        elif choice == "2":
            month_of_birth()
        elif choice == "3":
            add_new_actor()
        elif choice == "4":
            view_married_actors()
        elif choice == "5":
            add_actor_marriage()
        elif choice == "6":
            view_studios()
        elif choice == "x":
            print("Goodbye!")
            break
        else:
            print(f"Option not implemented yet. Try 1 or x for now.\n")
    return
    

if __name__ == "__main__":
	menu()