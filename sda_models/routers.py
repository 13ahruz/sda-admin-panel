class SDARouter:
    """
    A router to control all database operations on models for the
    SDA application. This ensures Django doesn't try to create
    migrations for tables that already exist from FastAPI/SQLAlchemy.
    """
    
    route_app_labels = {'sda_models'}

    def db_for_read(self, model, **hints):
        """Suggest the database that should be read from for objects of type model."""
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """Suggest the database that should be used for writes of objects of type model."""
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if a model in the SDA app is involved."""
        db_set = {'default'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the SDA app's models get created on the right database."""
        if app_label in self.route_app_labels:
            # Don't create migrations for our existing tables
            return False
        # Allow Django's built-in apps to create their tables
        return True
