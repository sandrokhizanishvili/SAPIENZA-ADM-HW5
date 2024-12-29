import heapq
import pandas as pd

def find_best_route(flights_df, origin_city, destination_city, date):
    """
    Find the best flight routes between two cities on a given date using Dijkstra's algorithm.

    Args:
        flights_df (pd.DataFrame): A DataFrame containing flight information. 
            Must include columns:
            - 'Fly_date': Date of the flight.
            - 'Origin_airport': Code of the origin airport.
            - 'Destination_airport': Code of the destination airport.
            - 'Distance': Distance between the airports.
            - 'Origin_city': Name of the city where the flight originates.
            - 'Destination_city': Name of the city where the flight lands.
        origin_city (str): Name of the origin city.
        destination_city (str): Name of the destination city.
        date (str): The date for which to find flights (format: YYYY-MM-DD).

    Returns:
        pd.DataFrame: A DataFrame containing the best routes for all origin-destination airport pairs.
            Columns:
            - 'Origin_city_airport': Airport code of the origin city.
            - 'Destination_city_airport': Airport code of the destination city.
            - 'Best_route': Shortest route as a string or 'No route found' if no route exists.
    """
    # Filter the flights dataset for the given date
    flights_df = flights_df[flights_df['Fly_date'] == date]
    
    # Create a dictionary for the graph
    graph = {}

    # Add edges to the graph
    for _, row in flights_df.iterrows():
        origin = row['Origin_airport']
        destination = row['Destination_airport']
        distance = row['Distance']
        
        if origin not in graph:
            graph[origin] = []
        graph[origin].append((destination, distance))
    
    # Get the airports for the origin and destination cities
    origin_airports = flights_df[flights_df['Origin_city'] == origin_city]['Origin_airport'].unique()
    destination_airports = flights_df[flights_df['Destination_city'] == destination_city]['Destination_airport'].unique()

    def dijkstra(start, target):
        """
        Perform Dijkstra's algorithm to find the shortest path between two airports.

        Args:
            start (str): The starting airport code.
            target (str): The target airport code.

        Returns:
            list or None: The shortest path as a list of airport codes, or None if no path exists.
        """
        # Min-heap for the priority queue
        pq = [(0, start, [])]  # (distance, current_node, path_taken)
        visited = set()

        while pq:
            current_distance, current_node, path = heapq.heappop(pq)

            # If the destination is reached, return the path
            if current_node == target:
                return path + [current_node]

            if current_node not in visited:
                visited.add(current_node)

                for neighbor, weight in graph.get(current_node, []):
                    if neighbor not in visited:
                        heapq.heappush(pq, (current_distance + weight, neighbor, path + [current_node]))

        return None  # No path found

    results = []

    # Compute the best route for every pair of origin and destination airports
    for origin_airport in origin_airports:
        for destination_airport in destination_airports:
            shortest_path = dijkstra(origin_airport, destination_airport)
            if shortest_path:
                results.append({
                    'Origin_city_airport': origin_airport,
                    'Destination_city_airport': destination_airport,
                    'Best_route': ' -> '.join(shortest_path)
                })
            else:
                results.append({
                    'Origin_city_airport': origin_airport,
                    'Destination_city_airport': destination_airport,
                    'Best_route': 'No route found'
                })

    # Convert results into a DataFrame and return
    result_df = pd.DataFrame(results)
    return result_df
