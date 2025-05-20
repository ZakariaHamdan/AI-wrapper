using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Domain.Abstractions;
using BuildingBlock.Core.Workflow.Abstractions;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class MainEntity : AuditedEntity<Guid>
{
    public Status Status { get; set; } = Status.Pending;
}
