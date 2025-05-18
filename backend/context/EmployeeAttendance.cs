using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Entities.Interfaces;

namespace RSG.Biovision.Domain.Entities;

public class EmployeeAttendance : MainEntity , IHasCompany
{
    [Required]
    public Guid EmployeeId { get; set; }

    [Required]
    public DateTime AttendanceDate { get; set; }
    
    public bool HasSchedule { get; set; } = true;
    public Guid? ScheduleId { get; set; }
    public Guid CompanyId { get; set; }

    public Guid? ShiftId { get; set; }

    public DateTime? TimeIn { get; set; }
    public DateTime? TimeOut { get; set; }
    public DateTime? BreakFrom { get; set; }
    public DateTime? BreakTo { get; set; }

    [Required]
    [Column(TypeName = "decimal(18, 2)")]
    public decimal TotalWorkHours { get; set; }

    [Required]
    [Column(TypeName = "decimal(18, 2)")]
    public decimal ApprovedWorkHours { get; set; }

    [Required]
    [Column(TypeName = "decimal(18, 2)")]
    public decimal TotalOverTime { get; set; }

    [Required]
    [Column(TypeName = "decimal(18, 2)")]
    public decimal ApprovedOverTime { get; set; }

    [Required]
    public int AttendanceStatus { get; set; }   // To Enum 

    [Required]
    public DateTime TransactionDate { get; set; }

    [Required]
    public bool HasException { get; set; }

    [Required]
    public bool IsActualBreak { get; set; }

    [Required]
    [Column(TypeName = "decimal(18, 2)")]
    public decimal ScheduleWorkHours { get; set; }

    [Required]
    public bool IsReseted { get; set; }

    [Required]
    public bool IsPublicHoliday { get; set; }

    [Required]
    [Column(TypeName = "decimal(18, 2)")]
    public decimal BreakDeductionHours { get; set; }

    public Guid? ProjectId { get; set; }

    public string ScheduleType { get; set; } = null!;

    public string? HolidayCondition { get; set; }

    public bool IsHoliday { get; set; }

    public int Source { get; set; }

    [ForeignKey("EmployeeId")]
    public Employee Employee { get; set; } = null!;
    
    [ForeignKey("CompanyId")]
    public Company Company { get; set; } = null!;

    [ForeignKey("ScheduleId")]
    public Schedule? Schedule { get; set; }

    [ForeignKey("ShiftId")]
    public Shift? Shift { get; set; }
    
    [ForeignKey("ProjectId")]
    public Project? Project { get; set; }
}