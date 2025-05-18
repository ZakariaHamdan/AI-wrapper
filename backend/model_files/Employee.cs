using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Entities.Interfaces;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class Employee : MainEntity , IHasCompany
{
    [Required] [MaxLength(255)]
    public string Name { get; set; }
    public string? ReferenceNo { get; set; }
    public bool HasUserAccount { get; set; } = false;
    public bool HasSchedule { get; set; } = true;
    public Guid CompanyId { get; set; }
    public Guid? UserDetailId { get; set; }
    public Guid? ScheduleId { get; set; }
    public Guid SubContractorId { get; set; }
    public Guid ProjectId { get; set; }
    public Guid CategoryId { get; set; }
    public Guid SpecificationId { get; set; }
    public Guid PositionId { get; set; }
    public bool AllowGeoPunching { get; set; } = false;
    public string? DeviceToken { get; set; }
    public string? DeviceType { get; set; }
    public string? DeviceId { get; set; }
    public DateTime? DeviceLastActive { get; set; }

    [ForeignKey("CompanyId")] public Company Company { get; set; } = null!;
    [ForeignKey("UserDetailId")] public UserDetail? UserDetail { get; set; }
    [ForeignKey("ScheduleId")] public Schedule? Schedule { get; set; }
    [ForeignKey("SubContractorId")] public SubContractor SubContractor { get; set; } = null!;
    [ForeignKey("ProjectId")] public Project Project { get; set; } = null!;
    [ForeignKey("CategoryId")] public Category Category { get; set; } = null!;
    [ForeignKey("SpecificationId")] public Specification Specification { get; set; } = null!;
    [ForeignKey("PositionId")] public Position Position { get; set; } = null!;
    public virtual ICollection<ShiftAssignment> ShiftAssignments { get; set; } = new List<ShiftAssignment>();
    public ICollection<EmployeeSite> EmployeeSites { get; set; } = new List<EmployeeSite>();

}