using System.ComponentModel.DataAnnotations;
using RSG.Biovision.Domain.Entities.Interfaces;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class Schedule : MainEntity, IHasCompany
{
    [Required]
    [MaxLength(255)]
    public string? Name { get; set; }
    
    [Required]
    public TimeSpan StartTime { get; set; }
    public TimeSpan EndTime { get; set; }
    
    public int BufferStartMinutes { get; set; }
    public int BufferEndMinutes { get; set; }
    
    public int MinCheckInHours { get; set; }
    public int MaxCheckOutHours { get; set; }
    
    public bool IsHolidayPaid { get; set; }
    public string? HolidayConditions { get; set; }
    
    public Guid CompanyId { get; set; }
    public Guid? ProjectId { get; set; }
    
    // Navigation Properties
    public Company Company { get; set; } = null!;
    public Project? Project { get; set; }
    
    public virtual ICollection<ScheduleDay> WorkingDays { get; set; } = new List<ScheduleDay>();
    public List<Employee> Employees { get; set; } = new ();
}