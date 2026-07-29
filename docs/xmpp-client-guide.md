# Discovering and Invoking Remote Agent Tools over XMPP

This guide describes the client side of the XMPP Agent Gateway ProtoXEP:
discovering a gateway, selecting an agent endpoint and immutable API version,
retrieving a tool schema, invoking the tool, and recovering its result.

The
[ProtoXEP source](../protoxep-xmpp-agent-gateway.xml)
is authoritative. This guide intentionally focuses on the normal caller flow
and does not replace the protocol's normative requirements, schemas, security
considerations, or error rules.

## Protocol flow

An XMPP client follows this sequence:

```text
discover gateway
  -> list visible endpoint JIDs
  -> inspect endpoint features
  -> retrieve and pin the active manifest version and hash
  -> list tools for that exact version
  -> inspect a tool and retrieve its input schema
  -> validate arguments
  -> invoke with the pinned version and manifest hash
  -> persist the accepted task ID
  -> process best-effort lifecycle events
  -> recover authoritative state and terminal result with IQs
```

All endpoint addresses in this protocol are bare JIDs. Use full JIDs only as
the caller address and as the best-effort notification route.

## Namespaces and features

| Purpose | Namespace or feature |
| --- | --- |
| Agent directory | `urn:xmpp:agent-directory:0` |
| Endpoint marker | `urn:xmpp:agent-endpoint:0` |
| Agent manifests and schemas | `urn:xmpp:agent-api:0` |
| Manifest retrieval | `urn:xmpp:agent-api:0#manifest` |
| Schema retrieval | `urn:xmpp:agent-api:0#schema` |
| Version-pinned tool collection | `urn:xmpp:agent-tools:0#VERSION` |
| Tool metadata | `urn:xmpp:agent-tool:0` |
| Task execution | `urn:xmpp:agent-task:0` |
| Progress events | `urn:xmpp:agent-task:0#progress` |
| Cancellation | `urn:xmpp:agent-task:0#cancel` |
| Interactive input | `urn:xmpp:agent-task:0#input` |
| Service discovery | `http://jabber.org/protocol/disco#info` and `http://jabber.org/protocol/disco#items` |
| Result-set paging | `http://jabber.org/protocol/rsm` |
| Hashes | `urn:xmpp:hashes:2` |

Feature advertisement is authoritative. Do not infer support from a hostname,
JID localpart, display name, or previous response.

For optional task behavior, require support at both levels:

1. the endpoint advertises the corresponding feature; and
2. the selected version-pinned tool advertises or declares the same behavior.

## 1. Discover a gateway

If the gateway JID is already configured, query it directly with
`disco#info`. Otherwise, query the connected account's server with
`disco#items`:

```xml
<iq from='juliet@example.net/phone'
    id='services-1'
    to='example.net'
    type='get'>
  <query xmlns='http://jabber.org/protocol/disco#items'/>
</iq>
```

Treat each returned service JID only as a candidate. Query the candidate:

```xml
<iq from='juliet@example.net/phone'
    id='gateway-info-1'
    to='agents.example'
    type='get'>
  <query xmlns='http://jabber.org/protocol/disco#info'/>
</iq>
```

Accept it as an agent gateway only when the response contains:

```xml
<identity category='automation' type='agent-gateway'/>
<feature var='urn:xmpp:agent-directory:0'/>
```

The response can also advertise search, administration, ping, and other
profiles. Their presence does not grant permission to use them.

For federation, a client can query a known remote gateway in the same way.
Normal XMPP server-to-server authentication establishes the immediate sender,
but the remote gateway's policy still decides visibility and invocation
permission.

## 2. List visible agent endpoints

Send a paged `disco#items` request to the gateway's directory node:

```xml
<iq from='juliet@example.net/phone'
    id='agents-1'
    to='agents.example'
    type='get'>
  <query xmlns='http://jabber.org/protocol/disco#items'
         node='urn:xmpp:agent-directory:0'>
    <set xmlns='http://jabber.org/protocol/rsm'>
      <max>50</max>
    </set>
  </query>
</iq>
```

Each returned item identifies an endpoint by bare JID:

```xml
<item jid='weather@agents.example' name='Weather Agent'/>
```

Use XEP-0059 paging until the directory is exhausted. The normalized endpoint
bare JID is the stable RSM item ID. A gateway can return fewer entries than
requested.

An empty result means only that no endpoints are visible to this requester. It
does not prove that the gateway hosts no endpoints.

## 3. Inspect the endpoint

Query the selected endpoint's node-less `disco#info`:

```xml
<iq from='juliet@example.net/phone'
    id='endpoint-info-1'
    to='weather@agents.example'
    type='get'>
  <query xmlns='http://jabber.org/protocol/disco#info'/>
</iq>
```

Verify the endpoint identity and the profiles required by the application:

```xml
<identity category='automation' type='agent-endpoint'/>
<feature var='urn:xmpp:agent-endpoint:0'/>
<feature var='urn:xmpp:agent-api:0#manifest'/>
<feature var='urn:xmpp:agent-api:0#schema'/>
<feature var='urn:xmpp:agent-task:0'/>
```

Read the XEP-0128 result form whose `FORM_TYPE` is
`urn:xmpp:agent-endpoint-info:0`. Important fields are:

| Field | Client use |
| --- | --- |
| `server_name` | Stable implementation-oriented name |
| `server_title` | Human-readable title |
| `description` | Optional description |
| `version` | Currently selected manifest/API version |
| `manifest_hash_algo` | Manifest hash algorithm; version 0 requires `sha-256` |
| `manifest_hash_value` | Base64-encoded manifest hash |
| `cold_start_supported` | Whether invocation can wake an inactive runtime |
| `request_replay_seconds` | Minimum request-ID replay window |

Treat names, descriptions, and side-effect annotations as untrusted display
metadata. They are not authorization statements.

## 4. Retrieve and pin the manifest

Request the active manifest:

```xml
<iq from='juliet@example.net/phone'
    id='manifest-1'
    to='weather@agents.example'
    type='get'>
  <manifest-request xmlns='urn:xmpp:agent-api:0'/>
</iq>
```

A successful response contains the selected immutable version, manifest hash,
and canonical JSON:

```xml
<iq from='weather@agents.example'
    id='manifest-1'
    to='juliet@example.net/phone'
    type='result'>
  <manifest xmlns='urn:xmpp:agent-api:0'
            media-type='application/json'
            version='1.4.0'>
    <hash xmlns='urn:xmpp:hashes:2'
          algo='sha-256'>K2/YdwvIBAlfUIeZHiNCyiYA4m4W2wrEOqXQDoQyXp4=</hash>
    <json>{"agent":{"jid":"weather@agents.example","name":"weather","version":"1.4.0"},"manifestSpecVersion":"0","tools":[]}</json>
  </manifest>
</iq>
```

Persist these values together:

- endpoint bare JID;
- exact, case-sensitive API version;
- manifest hash algorithm and value; and
- canonical manifest JSON.

Verify that the JSON character data, after XML character extraction, hashes to
the advertised value using RFC 8785 canonical JSON and XEP-0300 hash encoding.
The version and hash returned here select all subsequent tool metadata,
schemas, and invocation behavior.

Do not continue with an endpoint-info version combined with a different
manifest hash. If the active version changes during discovery, restart from
manifest retrieval and pin the newly returned object.

## 5. List tools for the pinned version

Build the collection node by appending the exact version to
`urn:xmpp:agent-tools:0#`:

```xml
<iq from='juliet@example.net/phone'
    id='tools-1'
    to='weather@agents.example'
    type='get'>
  <query xmlns='http://jabber.org/protocol/disco#items'
         node='urn:xmpp:agent-tools:0#1.4.0'>
    <set xmlns='http://jabber.org/protocol/rsm'>
      <max>50</max>
    </set>
  </query>
</iq>
```

A returned tool item looks like:

```xml
<item jid='weather@agents.example'
      name='Get Forecast'
      node='urn:xmpp:agent-tool:0#1.4.0#Zm9yZWNhc3QuZ2V0'/>
```

The final node component is the unpadded RFC 4648 base64url encoding of the
exact UTF-8 tool name. Prefer the node returned by the endpoint over
reconstructing it from the display name.

Tool listing is also RSM-paged. The complete tool node is the stable RSM item
ID, and counts include only tools visible to the requester.

## 6. Retrieve tool metadata

Query the returned version-pinned tool node:

```xml
<iq from='juliet@example.net/phone'
    id='tool-info-1'
    to='weather@agents.example'
    type='get'>
  <query xmlns='http://jabber.org/protocol/disco#info'
         node='urn:xmpp:agent-tool:0#1.4.0#Zm9yZWNhc3QuZ2V0'/>
</iq>
```

Verify:

```xml
<identity category='automation' type='agent-tool'/>
<feature var='urn:xmpp:agent-tool:0'/>
```

Read the result form whose `FORM_TYPE` is
`urn:xmpp:agent-tool-info:0`. It provides:

- the exact tool `name`;
- optional `title` and `description`;
- the exact `api_version`;
- the required input-schema hash;
- an optional output-schema hash; and
- optional MCP side-effect hints such as `read_only`, `destructive`,
  `idempotent`, and `open_world`.

Confirm that the returned `api_version` is the pinned version and that the
input-schema hash pair is complete. Optional annotations are hints only. For
example, `read_only=1` does not prove that execution has no side effects.

## 7. Retrieve and validate the input schema

Request the input schema using the exact tool name, version, and pinned
manifest hash:

```xml
<iq from='juliet@example.net/phone'
    id='schema-1'
    to='weather@agents.example'
    type='get'>
  <schema-request xmlns='urn:xmpp:agent-api:0'
                  direction='input'
                  tool='forecast.get'
                  version='1.4.0'>
    <hash xmlns='urn:xmpp:hashes:2'
          algo='sha-256'>K2/YdwvIBAlfUIeZHiNCyiYA4m4W2wrEOqXQDoQyXp4=</hash>
  </schema-request>
</iq>
```

The response contains separate manifest and schema hashes:

```xml
<schema xmlns='urn:xmpp:agent-api:0'
        direction='input'
        media-type='application/schema+json'
        tool='forecast.get'
        version='1.4.0'>
  <manifest-hash>
    <hash xmlns='urn:xmpp:hashes:2'
          algo='sha-256'>K2/YdwvIBAlfUIeZHiNCyiYA4m4W2wrEOqXQDoQyXp4=</hash>
  </manifest-hash>
  <schema-hash>
    <hash xmlns='urn:xmpp:hashes:2'
          algo='sha-256'>XxGP62PwgOW9NLxx8ysunvuijMhSd0y4j1SSRTAbt7c=</hash>
  </schema-hash>
  <json>{"additionalProperties":false,"properties":{"city":{"type":"string"}},"required":["city"],"type":"object"}</json>
</schema>
```

Before invoking:

1. confirm the endpoint, tool, version, direction, and manifest hash;
2. compare the schema hash with tool discovery metadata;
3. verify the canonical schema bytes against the schema hash;
4. parse it as JSON Schema 2020-12; and
5. validate the argument object locally.

The target repeats validation authoritatively. Local validation improves the
user experience but does not replace target-side validation.

Do not automatically resolve external JSON Schema references. External
references require an explicit allowlist and resource budget.

## 8. Invoke the tool

Generate a cryptographically random request ID containing at least 128 bits of
unpredictability. It must be 22 to 128 characters from
`[A-Za-z0-9._~-]`.

Send an IQ of type `set` to the endpoint bare JID:

```xml
<iq from='planner@agents.example/worker'
    id='invoke-1'
    to='weather@agents.example'
    type='set'>
  <invoke xmlns='urn:xmpp:agent-task:0'
          api-version='1.4.0'
          request-id='req-91a6d2f49c514f44a2d223f0f97bd9fe'
          tool='forecast.get'>
    <manifest-hash>
      <hash xmlns='urn:xmpp:hashes:2'
            algo='sha-256'>K2/YdwvIBAlfUIeZHiNCyiYA4m4W2wrEOqXQDoQyXp4=</hash>
    </manifest-hash>
    <arguments media-type='application/json'>{"city":"Riga"}</arguments>
    <deadline>2026-07-27T19:15:00Z</deadline>
  </invoke>
</iq>
```

The `deadline` is optional. When present, it uses XEP-0082 date-time syntax.

An IQ result containing `accepted` means the target durably admitted the task:

```xml
<iq from='weather@agents.example'
    id='invoke-1'
    to='planner@agents.example/worker'
    type='result'>
  <accepted xmlns='urn:xmpp:agent-task:0'
            created='2026-07-27T19:14:01Z'
            request-id='req-91a6d2f49c514f44a2d223f0f97bd9fe'
            retain-until='2026-07-28T19:14:01Z'
            revision='0'
            task-id='task-7f2a9c41d8804e96bb478af6453c0371'/>
</iq>
```

Persist at least:

- caller bare JID;
- endpoint bare JID;
- request ID and the complete request fingerprint inputs;
- receiver-generated task ID;
- API version and manifest hash;
- current revision, initially `0`;
- creation time and `retain-until`; and
- deadline, if supplied.

A pre-admission IQ error means no task was created. A timeout or stream loss
does not mean that admission failed.

### Safe admission retry

If the acceptance IQ is lost, resend the identical request:

- same authenticated caller and target;
- same request ID;
- same tool, API version, and manifest hash;
- byte-equivalent canonical arguments;
- same deadline; and
- same security-relevant extensions.

During the advertised replay window, the target returns the original accepted
task without executing the tool twice. Reusing the request ID with any
fingerprint difference produces a `conflict` error.

Never create a fresh request ID merely because the IQ timed out. Reconcile the
original request first, especially for tools with external side effects.

## 9. Process lifecycle events

The target sends best-effort normal messages containing an `event` element:

```xml
<message from='weather@agents.example'
         id='progress-task-7f2a9c41d8804e96bb478af6453c0371'
         to='planner@agents.example/worker'
         type='normal'>
  <event xmlns='urn:xmpp:agent-task:0'
         event-id='evt-50a26b5692644a7880caa7ca56ca5b54'
         revision='2'
         task-id='task-7f2a9c41d8804e96bb478af6453c0371'
         type='progress'>
    {"percent":50,"stage":"fetch","message":"Forecast received"}
  </event>
</message>
```

Supported event types are:

| Type | Meaning |
| --- | --- |
| `status` | State changed to `running`, `input_required`, or `cancelling` |
| `progress` | Progress percentage, stage, or message |
| `input_required` | Caller input is required |
| `completed` | Terminal success with the complete result envelope |
| `failed` | Terminal execution failure |
| `cancelled` | Terminal cancellation |

For every event:

1. verify the authenticated sender is the expected endpoint;
2. locate the persisted task by endpoint bare JID and task ID;
3. validate the event JSON against the normative event schema;
4. require the next revision for a new event;
5. ignore an exact replay; and
6. ignore and log a repeated revision with a different event ID or payload.

A revision gap indicates lost notifications, not task failure. Query complete
task state instead of guessing the missing transition.

A `completed` event contains the complete result envelope. MCP bridges preserve
`content`, `structuredContent`, `isError`, and `_meta`. A result with
`isError=true` is still a completed tool call; it is not an infrastructure
`failed` state.

## 10. Recover authoritative state

Notifications are advisory. Task state and result IQs are the source of truth.

Query state after reconnecting, after a revision gap, or when a local wait
expires:

```xml
<iq from='planner@agents.example/worker'
    id='task-state-1'
    to='weather@agents.example'
    type='get'>
  <task-state-request xmlns='urn:xmpp:agent-task:0'
                      task-id='task-7f2a9c41d8804e96bb478af6453c0371'/>
</iq>
```

The `task-state` response supplies the current state and revision, pinned API
version and manifest hash, timestamps, retention deadline, result
availability, and any complete pending input request.

When the state is terminal and `result-available` is true, retrieve the result:

```xml
<iq from='planner@agents.example/phone'
    id='task-result-1'
    to='weather@agents.example'
    type='get'>
  <task-result-request xmlns='urn:xmpp:agent-task:0'
                       task-id='task-7f2a9c41d8804e96bb478af6453c0371'/>
</iq>
```

A successful response contains the immutable terminal state and complete
retained payload:

```xml
<task-result xmlns='urn:xmpp:agent-task:0'
             media-type='application/json'
             revision='4'
             state='completed'
             task-id='task-7f2a9c41d8804e96bb478af6453c0371'>
  {"result":{"content":[{"type":"text","text":"Light rain, 18 C"}],
             "structuredContent":{"summary":"Light rain, 18 C"},
             "isError":false}}
</task-result>
```

Result retrieval before terminal settlement returns `unexpected-request`.
Nonexistent, expired, unauthorized, and cross-tenant task IDs all return the
same `item-not-found` error.

The target promises state and terminal-result availability only until
`retain-until`. Preserve any data the application needs for longer.

## Interactive input

If both the endpoint and tool support
`urn:xmpp:agent-task:0#input`, an `input_required` event contains a
task-unique request ID, question, JSON Schema, creation time, and optional
expiry.

Validate the user's answer against that schema, then send:

```xml
<iq from='planner@agents.example/worker'
    id='input-answer-1'
    to='weather@agents.example'
    type='set'>
  <provide-input xmlns='urn:xmpp:agent-task:0'
                 expected-revision='3'
                 request-id='input-a5128a63d64146d5a6ffac65bb20c348'
                 task-id='task-7f2a9c41d8804e96bb478af6453c0371'>
    <input media-type='application/json'>{"unit":"C"}</input>
  </provide-input>
</iq>
```

Only an authorized resource of the original caller bare JID can answer. If the
notification was lost, recover the complete pending request from `task-state`.
Interactive input is data entry; it is not a portable approval or
authorization grant.

## Cancellation

If both the endpoint and tool support
`urn:xmpp:agent-task:0#cancel`, request cancellation with the latest known
revision:

```xml
<iq from='planner@agents.example/worker'
    id='cancel-request-1'
    to='weather@agents.example'
    type='set'>
  <cancel xmlns='urn:xmpp:agent-task:0'
          expected-revision='4'
          task-id='task-7f2a9c41d8804e96bb478af6453c0371'>
    <reason>Trip was cancelled</reason>
  </cancel>
</iq>
```

Cancellation is advisory. An accepted request moves the task to `cancelling`;
the target later settles it as `cancelled`, `completed`, or `failed`.
Successful work can win a race with cancellation.

## Error handling

Before durable acceptance, failures are ordinary IQ errors:

| Stanza condition | Typical meaning |
| --- | --- |
| `bad-request` | Malformed JSON or invalid/missing identifiers or attributes |
| `forbidden` | Denied operation where existence disclosure is safe |
| `item-not-found` | Unknown, hidden, expired, or unauthorized object |
| `not-acceptable` | Schema mismatch, failed validation, unsupported version, or expired deadline |
| `conflict` | Manifest mismatch, replay mismatch, stale input, or conflicting state |
| `resource-constraint` | Rate limit, size limit, or capacity exhaustion |
| `service-unavailable` | Endpoint runtime or optional profile is unavailable |

After acceptance, execution failures arrive as a terminal `failed` event. Its
JSON includes a stable code, safe message, and `retryable` boolean. A
`retryable` failure does not authorize blind replay with a fresh request ID;
apply tool-specific reconciliation first.

Do not reveal hidden-resource existence through UI wording, timing
classification, or diagnostic logs. In particular, display
`item-not-found` without distinguishing nonexistent from unauthorized.

## Minimum client state

A robust implementation keeps the following records.

### Endpoint cache

- endpoint bare JID;
- verified service-discovery identities and features;
- manifest version, hash, canonical JSON, and retrieval time;
- tool nodes and metadata for that exact version; and
- input/output schemas and verified hashes.

Invalidate version-pinned discovery data when selecting a different manifest.
Do not silently combine data across versions.

### Task record

- caller and endpoint bare JIDs;
- request ID and exact replay inputs;
- task ID after acceptance;
- API version and manifest hash;
- state and latest revision;
- accepted, updated, deadline, and retention times;
- pending input, if any; and
- terminal result or failure.

Persist the task record before treating acceptance or a lifecycle transition as
locally committed.

## Client implementation checklist

- Verify gateway and endpoint features instead of inferring them.
- Treat endpoint and tool identifiers as case-sensitive protocol values where
  specified.
- Pin one immutable manifest version and hash across discovery and invocation.
- Verify manifest and schema hashes over RFC 8785 canonical JSON.
- Validate arguments locally and expect authoritative target validation.
- Generate unpredictable request IDs and preserve complete replay inputs.
- Treat acceptance as durable admission and pre-acceptance errors as no task.
- Deduplicate lifecycle events by endpoint, task ID, and revision.
- Recover state after gaps, reconnects, and local timeouts.
- Retrieve terminal results before `retain-until`.
- Keep discovery visibility separate from invocation authorization.
- Treat descriptions, annotations, schemas, arguments, and results as
  untrusted content.
- Bound stanza size, JSON parsing, JSON Schema evaluation, pending IQs, and
  retained task data.

## Further reading

- [Rendered XMPP Agent Gateway ProtoXEP](https://romanbsd.github.io/xmpp-agent-gateway/)
- [Service Discovery](https://romanbsd.github.io/xmpp-agent-gateway/#discovery)
- [Manifest Retrieval](https://romanbsd.github.io/xmpp-agent-gateway/#manifest-retrieval)
- [Tool Execution](https://romanbsd.github.io/xmpp-agent-gateway/#execution)
- [Task Recovery](https://romanbsd.github.io/xmpp-agent-gateway/#task-recovery)
- [Security Considerations](https://romanbsd.github.io/xmpp-agent-gateway/#security)
