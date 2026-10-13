---
title: Getting started with the Supabase .NET SDK
title_original: Getting started with the Supabase .NET SDK
date: '2026-10-26'
source: Supabase Blog
source_url: https://supabase.com/blog/getting-started-with-the-supabase-dotnet-sdk
author: ''
summary: '[翻译失败，原文如下]


  The Supabase .NET SDK is a C# client for your Supabase project.

  It gives you Auth, Database, Storage, Realtime, and Edge Functions behind...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-13T08:48:32.639263'
---

[翻译失败，原文如下]

The Supabase .NET SDK is a C# client for your Supabase project.
It gives you Auth, Database, Storage, Realtime, and Edge Functions behind one API and handles the communication with the Supabase Platform.

Version8.0.0has been released, along with a newSupabase.Extensions.DependencyInjectionpackage.
This post covers how to set the client up, and then walk through basic operations.

## What changed inv8.0.0#

If you are coming from a previous major version, a few things moved.
You do not need all the details to follow this tutorial, but they are worth knowing:

- Serialization moved from Newtonsoft.Json toSystem.Text.Json. Custom converters and[JsonProperty]attributes need theirSystem.Text.Jsonequivalents.
- Every service client now accepts an injectableHttpClientand supports opt-in retry with backoff.
- There is a new dependency injection package for ASP.NET Core, covered below.
- Packages target .NET Standard 2.1. That drops .NET Framework, which tops out at .NET Standard 2.0, so you need .NET Core 3.0+ or .NET 5+.

If you want to see the full list of changes, check therelease notes.
Themigration guidelists every breaking change you may encounter and how to handle them.

## Install the package#

Add the meta-package to your project.
It brings in all five service packages (Auth, Postgrest, Storage, Realtime, and Functions):

If you only need one service, reference it on its own instead, for exampleSupabase.Gotruefor Auth orSupabase.Postgrestfor the database.

## Define a model#

The SDK maps a table to a C# class.
A model derives fromBaseModeland uses attributes to link its properties to columns.

Here is atodostable that we will use in upcoming examples, withid,task, andis_complete:

## Set up the client#

### ASP.NET Core#

Install the dependency injection package:

Register the client inProgram.cs:

AddSupabaseregisters theSupabase.Clientas a scoped service, so you can inject it wherever you need: a minimal API endpoint, a controller, or your own service.

It also registers each sub-client on its own (IPostgrestClient,IGotrueClient<User, Session>,IStorageClient<Bucket, FileObject>,IFunctionsClient,IRealtimeClient<RealtimeSocket, RealtimeChannel>), so a class that touches one service can depend on that alone.

We built this extension to make it easy for you to setup the client, rather than having to wire it up yourself.
ASupabase.Clientbuilds its ownHttpClientwhen you construct it. If you register as scoped or transient, every resolution creates a freshHttpClient(and a fresh socket), which will exhausts the connection pool under load.AddSupabasewires the client throughIHttpClientFactoryso the handler is pooled and reused.
To keep this consistent, it replaces anyHttpClientyou pass throughconfigureOptions; your proxy, retry, Realtime, and other options still apply.

### Other apps#

Outside ASP.NET Core, in Console apps, Desktop, Mobile, or Unity, construct the client yourself and initialize it once:

InitializeAsyncrestores a saved session and, withAutoConnectRealtimeon, opens the Realtime connection.
The default session handler does not store anything, so to restore a sign-in after a restart, setSupabaseOptions.SessionHandlerto your own implementation that saves and loads the session.
Create the client once and reuse it in the app.
A new client per operation means a newHttpClienteach time, which is the same problem the DI package solves on the server.

## Run the common operations#

The examples below use asupabasevariable, which is aSupabase.Clientinstance.

### Query rows#

From<T>()opens a query on the table mapped byT.
You can then filter usingWhereand then callGetto execute the query.

Getreturns aModeledResponse<T>, and you can find the rows inModels:

### Insert#

Insertwrites a single model or a list:

### Update and delete#

There are two ways to update an entity, and both are valid.
It simply depends on whether you already have the row in hand.

If you already retrieved a model, change its properties and callUpdateon it.
A row returned fromGetcarries its own identity, so it knows which record to write:

If you don't have a model, you can use the query builder which saves you aGetquery.
Set the new values, filter the rows, and run it:

While this looks very familiar to how Entity Framework is built, it does not behave the same.
There is noDbContext, no change tracker, and noSaveChanges.
Changing a property on a model does nothing until you callUpdate, and each call is its own HTTP request.

### Authenticate a user#

Authentication lives onsupabase.Auth.
Sign a user up and in with email and password:

WithAutoRefreshTokenenabled, the client refreshes the access token before it expires and attaches it to your database and Storage calls, so Row-Level-Security applies to the signed-in user.
The samesupabase.Authsurface covers OAuth, magic links, phone, and SSO.

### Upload a file#

## A note on keys#

Version8.0.0added the new publishable and secret API keys, alongside the existing anon and service keys.

Use a publishable or anon key in anything that ships to users.
Keep secret and service keys on the server.
A service key bypasses Row Level Security, so it does not belong in a client app.
When you need that level of access, use a separate client for it.

## Next steps#

You now have a client set up and can run queries, auth, and Storage from .NET. From here:

- Browse theC# referencefor the full API.
- Read theDependencyInjection package READMEfor the ASP.NET Core details.
- Check theSDK repositoryfor examples and the changelog.

---

> 本文由AI自动翻译，原文链接：[Getting started with the Supabase .NET SDK](https://supabase.com/blog/getting-started-with-the-supabase-dotnet-sdk)
> 
> 翻译时间：2026-10-13 08:48
