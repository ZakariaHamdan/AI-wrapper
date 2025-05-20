using System.ComponentModel.DataAnnotations.Schema;

namespace RSG.Biovision.Domain.Entities;

public class ShiftAssignment : MainEntity
{
    public Guid EmployeeId { get; set; }
    public Guid ShiftScheduleId { get; set; }
    public Guid ShiftId { get; set; }
    
    public DateTime StartDate { get; set; }
    public DateTime? EndDate { get; set; }
    
    [ForeignKey("EmployeeId")]
    public Employee Employee { get; set; } = null!;
    public ShiftSchedule ShiftSchedule { get; set; } = null!;
    public Shift Shift { get; set; } = null!;
}