namespace RSG.Biovision.Domain.Entities;

public class ScheduleDay : MainEntity
{
    public Guid ScheduleId { get; set; }
    public DayOfWeek Day { get; set; }
    public TimeSpan StartTime { get; set; }
    public TimeSpan EndTime { get; set; }
    
    public int BreakDurationMinutes { get; set; }
    public bool IsBreakPaid { get; set; }
    
    public decimal OvertimeMultiplier { get; set; } = 1.0m;
    public int MaxOvertimeHours { get; set; }
    
    public bool IsWorkDay { get; set; } = true;
    
    public Schedule Schedule { get; set; } = null!;
}