#See https://aka.ms/containerfastmode to understand how Visual Studio uses this Dockerfile to build your images for faster debugging.
FROM mcr.microsoft.com/dotnet/aspnet:6.0-bullseye-slim AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:6.0-bullseye-slim AS build


WORKDIR /src
COPY ["src/dotnet-api/dotnet-api.csproj", "dotnet-api/"]


RUN dotnet restore "dotnet-api/dotnet-api.csproj"
COPY src/. .
WORKDIR "/src/dotnet-api/"

RUN dotnet build "dotnet-api.csproj" -c Debug -o /app/build

FROM build AS publish
RUN dotnet publish "dotnet-api.csproj" -c Debug -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
EXPOSE 80
EXPOSE 443

RUN apt update
RUN apt install -y curl unzip procps
RUN curl -sSL https://aka.ms/getvsdbgsh | bash /dev/stdin -v latest -l /vsdbg

ENTRYPOINT ["dotnet", "dotnet-api.dll"]