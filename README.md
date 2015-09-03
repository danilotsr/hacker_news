This is a REST API to provide stats on queries performed on hn.algolia.com.

This is a brief explanation on the files in this repository.

src/
├── hacker_news/
│   ├── constants.py
│   ├── index.py  -- Data structures to represent the search index
│   ├── settings.py -- Django-specific settings
│   ├── tests.py -- Unit tests, yay!
│   ├── urls.py  -- URL mapping to views
│   └── views.py  -- Api endpoints
└── manage.py  -- Django admin script

include/
└── hn_logs.tsv.gz  -- Compressed TSV file listing all queries in the past few days

Everything else is Django auto-generated file.

== Api endpoints ==

* GET /{api_version}/queries/count/{date_string}

For instance: GET /1/queries/count/2015
It returns the number of unique queries performed in 2015.

* GET /{api_version}/queries/popular/{date_string}?size={integer}

For instance: GET /1/queries/popular/2015-08?size=5
It returns the top 5 queries performed in August, 2015.

* POST /{api_version}/build_index

This re-generate the index from scratch by reading from the original TSV file.
An optional argument, "size", can be specified to control how many queries 
will be used in the index.

== Implementation details ==

I decided to optimize for response time on the Api endpoints: `count` and `popular`. My solution indexes a query by
all the six date terms available in a full date string: year, month, day, hour, minute and second. Besides, it seems the
Api doesn't support queries in a custom date range, like from August to September, 2015. A different data structure
would be necessary to support that use case.

The downside of my solution is using a lot of extra memory, as each query will be present in six different indexes. If
memory is a concern, it could keep less indexes per query, however operations across multisets would be necessary to
fullfil the `query` and `popular` Api endpoints, which would make them a bit slower.

Lastly, it would be possible to partition the data so that if the input becomes too large to be handled by a
single server, it could be distributed across many servers by sharding on query value, so hash(query) % number_of_shards
would determine the shard id for each query.

== Dependencies ==

* Python 3.4
* Django 1.8
