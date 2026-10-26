---
title: "The New HTTP QUERY Method: What RFC 10008 Changes for API Design"
slug: the-new-http-query-method
date: 2026-08-10
tags: [http, api-design, standards]
summary: "QUERY gives HTTP a standard way to send request bodies for read-only operations, reducing the long-running GET-vs-POST workaround problem for complex queries."
status: draft
repo_url: ""
---

# The New HTTP QUERY Method: What RFC 10008 Changes for API Design

In June 2026, the IETF published RFC 10008, which standardizes a new HTTP method: `QUERY`. The goal is practical: let clients send query input in the request body while keeping the operation explicitly **safe** and **idempotent**. In plain terms, `QUERY` gives teams a standards-based alternative when URL query strings are too long or awkward, but using `POST` for read operations creates semantic and caching ambiguity.

## What changed

RFC 10008 defines `QUERY` as a method where the target resource processes enclosed content and returns the result, similar to many existing `POST`-based search endpoints. The key difference is method semantics: `QUERY` is explicitly safe and idempotent, unlike `POST`.

The spec frames this as a gap between two existing patterns:

- `GET` is semantically right for reads, but large or structured query input can be difficult to encode in URLs.
- `POST` accepts a body and is commonly used for queries in practice, but it does not inherently signal read-only behavior.

By adding `QUERY`, the standards body formalizes a widely used real-world need instead of forcing developers to overload `POST` for retrieval.

## How QUERY works in practice

At the protocol level, `QUERY` behaves like a first-class HTTP method with explicit rules:

- Requests carry query input in the body, with required and validated `Content-Type` metadata.
- Responses are cacheable, but cache keys must account for request content and related metadata.
- Servers can return `Location` and `Content-Location` to provide GET-friendly URIs for equivalent resources or results.
- Resources can advertise supported query media types using a new `Accept-Query` response header.

A simplified request looks like this:

```http
QUERY /products/search HTTP/1.1
Host: api.example.com
Content-Type: application/json
Accept: application/json

{"filters":{"category":"laptops","ram_gb":16},"sort":"price_asc","limit":20}
```

This is exactly the kind of payload many teams already ship via `POST /search`. RFC 10008 gives that pattern a clearer contract for retries, intermediaries, and semantics.

## Why this matters for API teams

The biggest gain is semantic clarity. With `QUERY`, clients, gateways, and observability tools can distinguish read-style operations from state-changing writes without endpoint naming conventions doing all the work.

It also improves failure-handling logic. Because `QUERY` is idempotent, retries after transient network failures are safer than with generic `POST` assumptions. That matters for mobile networks, flaky edges, and distributed systems where retry policies are automatic.

Caching is another significant angle. RFC 10008 allows caching of `QUERY` responses, but it also acknowledges complexity: caches must include body content in the cache key. In many deployments, the practical pattern will likely be this:

1. Execute a `QUERY` with body content.
2. Receive a `Location` URI for the equivalent resource.
3. Use subsequent `GET` requests against that URI for simpler cache and conditional request behavior.

That sequence combines expressive query input with mature GET tooling.

## Constraints and adoption caveats

`QUERY` solves a protocol gap, but adoption is not automatic.

First, every hop in the request path must understand or at least safely forward the method: clients, API gateways, WAF rules, load balancers, and origin frameworks. Any component that only allowlists older methods can break requests.

Second, browser-based use has CORS implications. RFC 10008 notes that `QUERY` is not in the CORS-safelisted method set, so browser clients require preflight handling.

Third, API design discipline still matters. `QUERY` is for safe operations. If an endpoint mutates state, it should remain `POST`, `PUT`, `PATCH`, or `DELETE` as appropriate.

## The bigger trend

This standard reflects a broader shift in HTTP and API engineering: stop treating method semantics as optional metadata. Over time, teams have leaned on custom endpoint naming (`/search`, `/query`) and implicit contract docs to express intent. RFC 10008 moves some of that burden back into the protocol where tooling can reason about it consistently.

The method is already reflected in IANA registries for both HTTP methods (`QUERY`) and HTTP fields (`Accept-Query`), marking it as part of the formal ecosystem rather than an experimental extension.

## Why it matters

> QUERY gives API teams a standards-track way to support complex read operations without sacrificing HTTP semantics, making retries, caching strategy, and intent clearer across infrastructure layers.

## The takeaway

`QUERY` will not replace `GET` or `POST`, and it should not. Instead, it gives architects a better option for a specific, common case: read-only queries that need a request body. For teams building search-heavy APIs, analytics endpoints, or advanced filtering interfaces, RFC 10008 is a meaningful addition to the HTTP toolbox.

## Sources

- IETF Datatracker - RFC 10008: The HTTP QUERY Method (June 2026): https://datatracker.ietf.org/doc/rfc10008/
- RFC Editor - RFC 10008 (HTML): https://www.rfc-editor.org/rfc/rfc10008.html
- IANA - Hypertext Transfer Protocol (HTTP) Method Registry: https://www.iana.org/assignments/http-methods/http-methods.xhtml
- IANA - Hypertext Transfer Protocol (HTTP) Field Name Registry (`Accept-Query`): https://www.iana.org/assignments/http-fields/http-fields.xhtml
- MDN - HTTP request methods reference (context on common method semantics): https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods
