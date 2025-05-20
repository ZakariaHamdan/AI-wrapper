using BuildingBlock.Core.MultiTenancy;
using BuildingBlock.UnitOfWork.Abstractions;
using BuildingBlock.UnitOfWork.Interfaces;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using RSG.Biovision.Data.Configurations;
using RSG.Biovision.Domain.Entities;
using RSG.Biovision.Domain.Views;

namespace RSG.Biovision.Data;

public class BioVisionDbContext : BaseDbContext
{
    protected readonly IConfiguration Configuration;
    private readonly ITenantService _tenantService;

    public BioVisionDbContext(DbContextOptions<BioVisionDbContext> options, IConfiguration configuration,
        IAuditPropertySetter auditPropertySetter, ITenantService tenantService)
        : base(options, false, auditPropertySetter)
    {
        Configuration = configuration;
        _tenantService = tenantService;
    }
    

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured)
        {
            optionsBuilder
                .UseSqlServer(_tenantService.GetCurrentTenant().ConnectionString, 
                    sqlOptions => sqlOptions.CommandTimeout(120));
        }
        base.OnConfiguring(optionsBuilder);
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfiguration(new MainContractorProjectConfiguration());
        modelBuilder.ApplyConfiguration(new ProjectConfiguration());
        modelBuilder.ApplyConfiguration(new MainContractorConfiguration());
        modelBuilder.ApplyConfiguration(new UserDetailConfiguration());
        modelBuilder.ApplyConfiguration(new EmployeeConfiguration());
        modelBuilder.ApplyConfiguration(new ScheduleConfiguration());
        modelBuilder.ApplyConfiguration(new ShiftScheduleConfiguration());
        modelBuilder.ApplyConfiguration(new ShiftAssignmentConfiguration());
        
        modelBuilder.Entity<PunchLog>()
            .HasOne(p => p.Site)
            .WithMany()
            .HasForeignKey(p => p.SiteId)
            .OnDelete(DeleteBehavior.NoAction); // This prevents the cascade delete
        modelBuilder.Entity<EmployeeAttendanceDashboard>()
            .ToView("vw_EmployeeAttendanceDashboard")
            .HasKey(e => e.AttendanceId);
        
        base.OnModelCreating(modelBuilder);
    }
    
    public DbSet<EmployeeAttendanceDashboard> EmployeeAttendanceDashboards { get; set; }
    public DbSet<Currency> Currencies { get; set; }
    public DbSet<Country> Countries { get; set; }
    public DbSet<Region> Regions { get; set; }
    public DbSet<City> Cities { get; set; }
    public DbSet<Company> Companies { get; set; }
    public DbSet<Project> Projects { get; set; }
    
    public DbSet<Category> Categories { get; set; }
    public DbSet<Specification> Specifications { get; set; }
    public DbSet<Position> Positions { get; set; }

    public DbSet<Nationality> Nationalities { get; set; }
    public DbSet<UserDetail> UserDetails { get; set; }
    public DbSet<MainContractor> MainContractors { get; set; }
    public DbSet<SubContractorType> SubContractorTypes { get; set; }
    public DbSet<SubContractor> SubContractors { get; set; }
    public DbSet<Employee> Employees { get; set; }
    public DbSet<Device> Devices { get; set; }

    public DbSet<MainContractorProject> MainContractorProjects { get; set; }
    
    public DbSet<Schedule> Schedules { get; set; }
    public DbSet<ScheduleDay> ScheduleDays { get; set; }
    
    public DbSet<ShiftSchedule> ShiftSchedules { get; set; }
    public DbSet<Shift> Shifts { get; set; }
    public DbSet<ShiftAssignment> ShiftAssignments { get; set; }
    public DbSet<EmployeeAttendance> EmployeeAttendances { get; set; }
    public DbSet<Site> Sites { get; set; }
    public DbSet<PunchLog> PunchLogs { get; set; }
    public DbSet<EmployeeSite> EmployeeSites { get; set; }
    public DbSet<Notification> Notifications { get; set; }
    
}