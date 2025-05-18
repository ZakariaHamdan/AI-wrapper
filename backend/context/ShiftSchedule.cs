// Shift Management Module

using System.ComponentModel.DataAnnotations;
using RSG.Biovision.Domain.Entities.Interfaces;

namespace RSG.Biovision.Domain.Entities;

public class ShiftSchedule : MainEntity, IHasCompany
{
    [Required]
    [MaxLength(255)]
    public string Name { get; set; }
    
    public bool IsRotating { get; set; }
    public int RotationDays { get; set; }
    
    public int BufferStartMinutes { get; set; }
    public int BufferEndMinutes { get; set; }
    
    public bool IsHolidayPaid { get; set; }
    public string? HolidayConditions { get; set; }
    
    public Guid CompanyId { get; set; }
    public Guid? ProjectId { get; set; }
    
    // Navigation Properties
    public Company Company { get; set; } = null!;
    public Project? Project { get; set; }
    
    public virtual ICollection<Shift> Shifts { get; set; } = new List<Shift>();
    public virtual ICollection<ShiftAssignment> Assignments { get; set; } = new List<ShiftAssignment>();
}