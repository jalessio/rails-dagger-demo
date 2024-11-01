import dagger
from dagger import dag, function, object_type

DOCKER_IMAGE_TAG = "ttl.sh/hsoidgfha9pe8r9:1h"


@object_type
class Rails:
    @function
    def base(self, source: dagger.Directory) -> dagger.Container:
        """Returns base Docker image"""
        return source.docker_build()

    @function
    def publish_to_ttl(self, source: dagger.Directory) -> str:
        """Publishes the Docker image to ttl.sh"""
        return self.generate_schema_cache(source).publish(DOCKER_IMAGE_TAG)

    @function
    def generate_schema_cache(self, source: dagger.Directory) -> dagger.Container:
        """
        Demonstrate how to generate schema cache by running a command which produces
        a file on the filesystem and then publishing a Docker image with that file in it.
        """
        db = dag.mariadb().serve()

        return (
            self.base(source)
            .with_service_binding("db", db)
            .with_env_variable("DB_HOST", "db")
            .with_exec(["bundle", "exec", "rails", "db:create"])
            .with_exec(["bundle", "exec", "rails", "db:migrate"])
            .with_exec(
                [
                    "bundle",
                    "exec",
                    "rake",
                    "db:schema:cache:dump",
                ]
            )
        )

    @function
    def rails_test(self, source: dagger.Directory) -> str:
        """Demonstrate how to run Rails tests via Dagger using a MariaDB service"""
        db = dag.mariadb().serve()

        return (
            self.base(source)
            .with_service_binding("db", db)
            .with_env_variable("DB_HOST", "db")
            .with_exec(["bin/rails", "db:test:prepare"])
            .with_exec(["bin/rails", "test"])
            .stdout()
        )
