using System.ComponentModel.DataAnnotations;

namespace RSG.Biovision.Domain.Entities;

public class Shift : MainEntity
{
    public Guid ShiftScheduleId { get; set; }
    
    [Required]
    [MaxLength(255)]
    public string Name { get; set; }
    
    public int DayInRotation { get; set; } // Only used when ShiftSchedule.IsRotating is true
    public TimeSpan StartTime { get; set; }
    public TimeSpan EndTime { get; set; }
    
    public int BreakDurationMinutes { get; set; }
    public bool IsBreakPaid { get; set; }
    
    public decimal OvertimeMultiplier { get; set; } = 1.0m;
    public int MaxOvertimeHours { get; set; }
    
    public bool IsActive { get; set; } = true;
    
    public ShiftSchedule Schedule { get; set; } = null!;
    
    public virtual ICollection<ShiftAssignment> Assignments { get; set; } = new List<ShiftAssignment>();
}