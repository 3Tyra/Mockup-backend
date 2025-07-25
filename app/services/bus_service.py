from app.models.bus import Bus
from app.models.route import BusSchedule
from app.utils.database import db
from datetime import datetime

class BusService:
    @staticmethod
    def register_bus(driver_id, registration_number, capacity, make, model):
        # Check if bus already exists
        if Bus.query.filter_by(registration_number=registration_number).first():
            raise ValueError('Bus with this registration number already exists')
        
        # Create new bus
        bus = Bus(
            registration_number=registration_number,
            capacity=capacity,
            make=make,
            model=model,
            driver_id=driver_id
        )
        
        db.session.add(bus)
        db.session.commit()
        
        return bus

    @staticmethod
    def schedule_trip(bus_id, route_id, departure_time, arrival_time, price_per_seat, driver_id):
        # Check if bus belongs to driver
        bus = Bus.query.filter_by(id=bus_id, driver_id=driver_id).first()
        if not bus:
            raise ValueError('Bus not found or not owned by driver')
        
        # Convert string dates to datetime objects
        try:
            departure_dt = datetime.fromisoformat(departure_time)
            arrival_dt = datetime.fromisoformat(arrival_time)
        except ValueError:
            raise ValueError('Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)')
        
        # Create new schedule
        schedule = BusSchedule(
            bus_id=bus_id,
            route_id=route_id,
            departure_time=departure_dt,
            arrival_time=arrival_dt,
            price_per_seat=price_per_seat
        )
        
        db.session.add(schedule)
        db.session.commit()
        
        return schedule

    @staticmethod
    def get_available_buses(origin, destination, date):
        # Query buses with matching routes and schedules
        query = BusSchedule.query.join(Route).filter(
            Route.origin.ilike(f'%{origin}%'),
            Route.destination.ilike(f'%{destination}%'),
            func.date(BusSchedule.departure_time) == date
        ).all()
        
        return query