import logging

from redis import cluster

try:
  logging.info("Trying to connect to redis cluster")
  # @klotho::persist {
  #   id = "redis"
  # }
  client = cluster.RedisCluster(host='localhost', port=8001)
  logging.info("Connected to redis cluster")
except Exception as e:
  logging.error(e)
  raise(e)
