# Dagger + Ruby on Rails Demo

This is a demo of using [Dagger](https://dagger.io/) with a [Ruby on Rails](https://rubyonrails.org/) application.

**NOTE: You'll need Docker running on your system to run the example.**

## Dagger

The Dagger code of interest is located in `dagger/src/main/rails.py`.

To run the code there do the following:

### Install Dagger

Full installation instructions at [https://docs.dagger.io/install/](https://docs.dagger.io/install/). For quickstart on macOS run:

```
brew install dagger/tap/dagger
```

### Run Dagger Functions

Build a Docker image, generate a database schema cache file in the image, and publish the image to the ephemeral Docker registry at [https://ttl.sh/](https://ttl.sh/):

```
dagger call publish-to-ttl --source .
```

You can now pull that Docker image from anywhere in the world and work with it. Let's cat the contents of the db schema cache file:

```
docker run --pull=always --rm ttl.sh/hsoidgfha9pe8r9:1h cat db/schema_cache.yml
```

Run the `rails test` command inside of a Docker container that is built from the `Dockerfile` in this repo:

```
dagger call rails-test --source .
```
