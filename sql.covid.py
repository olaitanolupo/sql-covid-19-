Python 3.10.5 (v3.10.5:f377153967, Jun  6 2022, 12:36:10) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.

select *
from myportfolio1..coviddeaths$
order by 1,2


--select *
--from myportfolio1..covidvaccinations
--order by 1,2

select
location,date,total_cases,new_cases, total_deaths, population
from myportfolio1..coviddeaths$
where continent is not null
order by 1,2

select
location,date,total_cases,total_deaths,(total_deaths/total_cases)*100 as DeathPercentage
from  myportfolio1..coviddeaths$
where continent like '%africa%'
and continent is not null
order by 1,2


select
location,date,population,total_cases,(total_cases/population)*100 as PercentofInfected
from  myportfolio1..coviddeaths$
--where location like '%nigeria%'
order by 1,2

select location,population,DATE, Max(total_cases) as HighestInfectionCount, MAX((total_cases/population))*100 as PercentofInfected
from  myportfolio1..coviddeaths$
--where location like '%nigeria%'
--where continent is not null
group by location,population,date
order by PercentofInfected desc

select location,date,max(cast(total_deaths as int))TotalDeathCounts
from myportfolio1..coviddeaths$
--where location like %nigeria%
where continent is not null
and location not in ('world','european union','international')
group by location,date
order by TotalDeathCounts desc


--continent with highest death rate


select continent,max(cast(total_deaths as int))TotalDeathCounts
from  myportfolio1..coviddeaths$
--where location like '%nigeria%'
where continent is not null
group by continent
order by TotalDeathCounts desc


select SUM(new_cases) as total_cases,SUM(cast(new_deaths as int))as total_deaths,SUM(cast(new_deaths as int))/sum
(new_cases)*100 as DeathPercent
from  myportfolio1..coviddeaths$
--where location like '%nigeria%'
where continent is not null
order by 1,2



select dea.continent, dea.location, dea.date,dea.population,vac.new_vaccinations
,SUM(convert(bigint,vac.new_vaccinations)) Over (partition by dea.location order by dea.date)as RollingPeopleVaccinated
--(RollingPeopleVaccinated/population)*100
from myportfolio1..coviddeaths$ dea
join myportfolio1..covidvaccinations vac
on dea.location = vac.location
  and dea.date = vac.date
where dea.continent is not null
order by 1,2


--using CTE

with popvsvac(continent,location,date,population,new_vaccinations,RollingPeopleVaccinated)
as
(
select dea.continent, dea.location, dea.date,dea.population,vac.new_vaccinations
,SUM(convert(bigint,vac.new_vaccinations)) Over (partition by dea.location order by dea.date)as RollingPeopleVaccinated
--,(RollingPeopleVaccinated/population)*100
from myportfolio1..coviddeaths$ dea
join myportfolio1..covidvaccinations vac
on dea.location = vac.location
  and dea.date = vac.date
where dea.continent is not null
--order by 2,3
)
SELECT *,(RollingPeopleVaccinated/population)*100
FROM popvsvac


--TEMP TABLE

DROP TABLE if exists #Percentpopulationvaccinated
create table #Percentpopulationvaccinated
(
continent nvarchar (255),
location  nvarchar (255),
--date datetime,
population numeric,
new_vaccinations numeric,
RollingPeopleVaccinated numeric
)

insert into #Percentpopulationvaccinated

select dea.continent, dea.location,dea.population,vac.new_vaccinations
,SUM(convert(bigint,vac.new_vaccinations)) Over (partition by dea.location order by dea.date)as RollingPeopleVaccinated
--,(RollingPeopleVaccinated/population)*100
from myportfolio1..coviddeaths$ dea
join myportfolio1..covidvaccinations vac
       on dea.location = vac.location
  and dea.date = vac.date
--where dea.continent is not null
--order by 1,2

SELECT *,(RollingPeopleVaccinated/population)*100
FROM #Percentpopulationvaccinated


--CREATING VIEW FOR VISUALIZATION

create view populationvaccinated as

select dea.continent, dea.location,dea.population,vac.new_vaccinations
,SUM(convert(bigint,vac.new_vaccinations)) Over (partition by dea.location order by dea.date)as RollingPeopleVaccinated
--,(RollingPeopleVaccinated/population)*100
from myportfolio1..coviddeaths$ dea
join myportfolio1..covidvaccinations vac
       on dea.location = vac.location
  and dea.date = vac.date
where dea.continent is not null

select*
from populationvaccinated
--where location like '%nigeria%'